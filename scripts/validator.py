#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0", "detect-secrets>=1.4"]
# ///
"""Ansible Role Quality Validator - Measures PASS scores across six dimensions."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

THRESHOLDS = {"idempotency": 74, "security": 80, "module_selection": 81,
              "error_handling": 77, "structure": 91, "linting": 100}
STATE_MODULES = {"command", "shell", "raw", "script", "file", "copy", "template",
                 "lineinfile", "blockinfile", "apt", "yum", "dnf", "pip", "package",
                 "service", "systemd", "systemd_service", "user", "group"}
EXCUSED_CMDS = [r"pvecm\s+", r"pveceph\s+", r"pveum\s+", r"qm\s+", r"pct\s+",
                r"ceph\s+", r"ceph-volume\s+", r"microk8s\s+", r"kubectl\s+", r"helm\s+"]
SECRET_PATS = [r"password:\s*['\"]?[^{'\"\s]+", r"secret:\s*['\"]?[^{'\"\s]+",
               r"api_key:\s*['\"]?[^{'\"\s]+"]
DS_FP = ["secret_name", "secret_var_name", "infisical", "lookup(", "PROXMOX_",
         "sudo_nopasswd", "nopasswd", "NOPASSWD", "#", "{{", "defaults/main.yml",
         "sudo_config.yml", "msg:", "localhost", "127.0.0.1", "download.proxmox.com"]
META_KEYS = {"name", "when", "register", "loop", "loop_control", "notify", "tags",
             "vars", "environment", "become", "become_user", "delegate_to", "run_once",
             "changed_when", "failed_when", "ignore_errors", "no_log", "retries",
             "delay", "until", "block", "rescue", "always"}


@dataclass
class Issue:
    file: str
    line: int
    message: str
    def __str__(self) -> str:
        return f"{self.file}:{self.line} - {self.message}"


@dataclass
class DimResult:
    score: int
    passed: bool
    issues: list[Issue] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"pass": self.passed, "score": self.score, "issues": [str(i) for i in self.issues]}


@dataclass
class Result:
    role: str
    scenario: str
    timestamp: str
    dimensions: dict[str, DimResult]
    overall_pass: bool
    overall_score: int
    def to_dict(self) -> dict:
        return {"role": self.role, "scenario": self.scenario, "timestamp": self.timestamp,
                "dimensions": {k: v.to_dict() for k, v in self.dimensions.items()},
                "overall_pass": self.overall_pass, "overall_score": self.overall_score}


def load_yaml(path: Path) -> list[dict] | None:
    try:
        for d in yaml.safe_load_all(path.read_text()):
            if d:
                return d if isinstance(d, list) else [d]
        return []
    except Exception:
        return None


def find_tasks(role: Path) -> list[Path]:
    d = role / "tasks"
    return list(d.glob("*.yml")) + list(d.glob("*.yaml")) if d.exists() else []


def line_map(path: Path) -> dict[int, int]:
    m, idx = {}, 0
    for i, ln in enumerate(path.read_text().split("\n"), 1):
        s = ln.lstrip()
        if s.startswith("- name:") or s.startswith("- ansible.") or (s.startswith("- ") and ":" in s):
            m[idx], idx = i, idx + 1
    return m


def get_module(task: dict) -> str:
    for k in task:
        if k not in META_KEYS:
            return k
    return ""


def analyze_idempotency(role: Path) -> DimResult:
    issues, pos, neg, cnt = [], 0, 0, 0
    for tf in find_tasks(role):
        tasks = load_yaml(tf)
        if not tasks:
            continue
        lm, rel = line_map(tf), tf.relative_to(role)
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                continue
            ln, mod = lm.get(i, i + 1), get_module(t)
            if mod not in STATE_MODULES:
                continue
            cnt += 1
            if t.get("changed_when") is False:
                pos += 20
            elif "changed_when" in t:
                pos += 20
            args = t.get(mod, {})
            if isinstance(args, dict) and (args.get("creates") or args.get("removes")):
                pos += 20
            if t.get("register") and t.get("when"):
                pos += 10
            if mod in ("command", "shell"):
                has_guard = "changed_when" in t or t.get("when")
                cmd = str(t.get(mod, args.get("cmd", "") if isinstance(args, dict) else ""))
                if not has_guard and not any(re.search(p, cmd) for p in EXCUSED_CMDS):
                    neg, issues = neg - 15, issues + [Issue(str(rel), ln, "command/shell without guard")]
    score = 100 if cnt == 0 else max(0, min(100, 50 + pos + neg))
    return DimResult(score, score >= THRESHOLDS["idempotency"], issues)


def analyze_security(role: Path) -> DimResult:
    issues, pos, neg = [], 0, 0
    for tf in find_tasks(role):
        tasks, content = load_yaml(tf), tf.read_text()
        if not tasks:
            continue
        rel = tf.relative_to(role)
        for t in tasks:
            if isinstance(t, dict):
                if t.get("no_log") is True:
                    pos += 10
                if "infisical" in str(t).lower():
                    pos += 5
        for ln_num, ln in enumerate(content.split("\n"), 1):
            if ln.strip().startswith("#"):
                continue
            for p in SECRET_PATS:
                if re.search(p, ln, re.I) and "{{" not in ln and "lookup(" not in ln:
                    neg, issues = neg - 20, issues + [Issue(str(rel), ln_num, "hardcoded secret")]
                    break
            if "http://" in ln and "https://" not in ln:
                if not any(e in ln for e in ["localhost", "127.0.0.1", "download.proxmox.com", "download.ceph.com"]):
                    neg, issues = neg - 10, issues + [Issue(str(rel), ln_num, "insecure http://")]
    try:
        r = subprocess.run(["detect-secrets", "scan", str(role), "--all-files"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            for fp, findings in json.loads(r.stdout).get("results", {}).items():
                try:
                    fc = Path(fp).read_text().split("\n")
                except Exception:
                    fc = []
                for f in findings:
                    ln = f.get("line_number", 0)
                    lc = fc[ln - 1] if 0 < ln <= len(fc) else ""
                    if not any(pat in lc or pat in fp for pat in DS_FP):
                        neg, issues = neg - 10, issues + [Issue(fp, ln, f"detect-secrets: {f.get('type', '?')}")]
    except Exception:
        pass
    score = max(0, min(100, 100 + pos + neg))
    return DimResult(score, score >= THRESHOLDS["security"], issues)


def analyze_modules(role: Path) -> DimResult:
    issues, fqcn, dep, total = [], 0, 0, 0
    deprecated = {"include", "synchronize", "docker", "ec2_facts"}
    for tf in find_tasks(role):
        tasks = load_yaml(tf)
        if not tasks:
            continue
        lm, rel = line_map(tf), tf.relative_to(role)
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                continue
            mod = get_module(t)
            if not mod:
                continue
            total += 1
            if "." in mod:
                fqcn += 1
            elif mod not in ("block", "rescue", "always", "include_tasks", "import_tasks"):
                issues.append(Issue(str(rel), lm.get(i, i + 1), f"non-FQCN: {mod}"))
            if mod in deprecated:
                dep, issues = dep + 1, issues + [Issue(str(rel), lm.get(i, i + 1), f"deprecated: {mod}")]
    score = 100 if total == 0 else max(0, min(100, int((fqcn / total) * 100) - dep * 30))
    return DimResult(score, score >= THRESHOLDS["module_selection"], issues)


def analyze_errors(role: Path) -> DimResult:
    issues, pos, neg, cnt = [], 0, 0, 0
    for tf in find_tasks(role):
        tasks = load_yaml(tf)
        if not tasks:
            continue
        lm, rel = line_map(tf), tf.relative_to(role)
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                continue
            cnt += 1
            if "block" in t and "rescue" in t:
                pos += 25
            if "failed_when" in t:
                pos += 15
            if t.get("ignore_errors") is True:
                if t.get("register"):
                    pos += 10
                else:
                    neg, issues = neg - 20, issues + [Issue(str(rel), lm.get(i, i + 1), "ignore_errors w/o register")]
    score = 100 if cnt == 0 else max(0, min(100, 85 + pos + neg))
    return DimResult(score, score >= THRESHOLDS["error_handling"], issues)


def analyze_structure(role: Path) -> DimResult:
    issues, pos, neg = [], 0, 0
    if (role / "defaults" / "main.yml").exists():
        pos += 10
    if (role / "handlers").exists() and list((role / "handlers").glob("*.yml")):
        pos += 10
    named, unnamed, tfc = 0, 0, len(find_tasks(role))
    for tf in find_tasks(role):
        tasks = load_yaml(tf)
        if not tasks:
            continue
        lm, rel = line_map(tf), tf.relative_to(role)
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                continue
            if t.get("name"):
                named += 1
            elif get_module(t) not in ("block", "rescue", "always"):
                unnamed, neg = unnamed + 1, neg - 15
                issues.append(Issue(str(rel), lm.get(i, i + 1), "unnamed task"))
    if tfc > 10:
        neg, issues = neg - (tfc - 10) * 5, issues + [Issue("role", 0, f"{tfc} task files")]
    total = named + unnamed
    if total > 0:
        pos += int((named / total) * 15)
    score = max(0, min(100, 70 + pos + neg))
    return DimResult(score, score >= THRESHOLDS["structure"], issues)


def analyze_linting(role: Path, cfg: Path | None = None) -> DimResult:
    if cfg is None:
        p = role
        while p != p.parent:
            for n in [".ansible-lint", ".ansible-lint.yml"]:
                if (p / n).exists():
                    cfg = p / n
                    break
            if cfg:
                break
            p = p.parent
    cmd = ["ansible-lint", str(role)] + (["-c", str(cfg)] if cfg else [])
    try:
        cwd = role.parent.parent if "roles" in str(role) else role.parent
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=cwd)
        v = len([ln for ln in r.stdout.split("\n") if ": " in ln and not ln.startswith(" ")])
        if r.returncode == 0 or v == 0:
            return DimResult(100, True, [])
        return DimResult(max(0, 100 - v * 5), False, [Issue("lint", 0, f"{v} violations")])
    except FileNotFoundError:
        return DimResult(100, True, [])
    except subprocess.TimeoutExpired:
        return DimResult(50, False, [Issue("validator", 0, "timeout")])


def validate(role: Path, cfg: Path | None = None) -> Result:
    s = str(role.resolve())
    if any(p in s for p in [".ansible/roles", "ansible_collections", ".cache/ansible-compat"]):
        return Result(role.name, role.name.replace("_", "-"), datetime.now(timezone.utc).isoformat(), {}, True, 100)
    dims = {"idempotency": analyze_idempotency(role), "security": analyze_security(role),
            "module_selection": analyze_modules(role), "error_handling": analyze_errors(role),
            "structure": analyze_structure(role), "linting": analyze_linting(role, cfg)}
    overall = sum(d.score for d in dims.values()) // len(dims)
    return Result(role.name, role.name.replace("_", "-"), datetime.now(timezone.utc).isoformat(),
                  dims, all(d.passed for d in dims.values()), overall)


def compare(base: Path, curr: Path) -> dict:
    with base.open() as f:
        b = json.load(f)
    with curr.open() as f:
        c = json.load(f)
    deltas = {d: {"baseline": b["dimensions"][d]["score"], "current": c["dimensions"][d]["score"],
                  "delta": c["dimensions"][d]["score"] - b["dimensions"][d]["score"]}
              for d in b.get("dimensions", {}) if d in c.get("dimensions", {})}
    return {"role": c.get("role"), "dimension_deltas": deltas,
            "overall_delta": c.get("overall_score", 0) - b.get("overall_score", 0)}


def fmt_table(r: Result) -> str:
    lines = [f"\nValidation Results: {r.role}", "=" * 60,
             f"{'Dimension':<20} {'Score':>6} {'Pass':>6} {'Issues':>8}", "-" * 60]
    for d, res in r.dimensions.items():
        lines.append(f"{d:<20} {res.score:>5}% {'PASS' if res.passed else 'FAIL':>6} {len(res.issues):>8}")
    lines += ["-" * 60, f"{'OVERALL':<20} {r.overall_score:>5}% {'PASS' if r.overall_pass else 'FAIL':>6}", "=" * 60]
    issues = [f"  [{d}] {i}" for d, res in r.dimensions.items() for i in res.issues[:3]]
    if issues:
        lines += ["\nTop Issues:"] + issues[:10]
    return "\n".join(lines)


def get_roles_dir() -> Path | None:
    rd = Path(__file__).parent.parent / "ansible" / "roles"
    return rd if rd.exists() else None


def main() -> int:
    p = argparse.ArgumentParser(description="Ansible Role Quality Validator")
    p.add_argument("--role", type=Path)
    p.add_argument("--dimension", choices=list(THRESHOLDS.keys()))
    p.add_argument("--all-roles", action="store_true")
    p.add_argument("--output", choices=["json", "table"], default="table")
    p.add_argument("--lint-config", type=Path)
    p.add_argument("--compare", nargs=2, metavar=("BASE", "CURR"))
    p.add_argument("--calibrate", action="store_true")
    args = p.parse_args()

    if args.compare:
        print(json.dumps(compare(Path(args.compare[0]), Path(args.compare[1])), indent=2))
        return 0

    if args.calibrate or args.all_roles:
        rd = get_roles_dir()
        if not rd:
            print("Error: roles directory not found", file=sys.stderr)
            return 2
        results = [validate(d, args.lint_config) for d in sorted(rd.iterdir())
                   if d.is_dir() and not d.name.startswith(".")]
        if args.calibrate:
            print("Calibration mode: Analyzing reference roles...")
            for r in results:
                print(f"  {r.role}: {r.overall_score}%")
            print("\nDimension Averages:")
            for d in THRESHOLDS:
                scores = [r.dimensions[d].score for r in results if d in r.dimensions]
                if scores:
                    print(f"  {d}: {sum(scores) / len(scores):.1f}%")
            return 0
        if args.output == "json":
            print(json.dumps([r.to_dict() for r in results], indent=2))
        else:
            for r in results:
                print(fmt_table(r))
        return 0 if all(r.overall_pass for r in results) else 1

    if not args.role:
        p.print_help()
        return 2
    if not args.role.exists() or not args.role.is_dir():
        print(f"Error: {args.role}", file=sys.stderr)
        return 2

    if args.dimension:
        analyzers = {"idempotency": analyze_idempotency, "security": analyze_security,
                     "module_selection": analyze_modules, "error_handling": analyze_errors,
                     "structure": analyze_structure, "linting": lambda r: analyze_linting(r, args.lint_config)}
        res = analyzers[args.dimension](args.role)
        if args.output == "json":
            print(json.dumps({args.dimension: res.to_dict()}, indent=2))
        else:
            print(f"\n{args.dimension}: {res.score}% ({'PASS' if res.passed else 'FAIL'})")
            for i in res.issues:
                print(f"  - {i}")
        return 0 if res.passed else 1

    r = validate(args.role, args.lint_config)
    print(json.dumps(r.to_dict(), indent=2) if args.output == "json" else fmt_table(r))
    return 0 if r.overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
