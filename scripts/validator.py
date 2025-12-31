#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0", "detect-secrets>=1.4"]
# ///
"""Ansible Role Quality Validator - Calibrated PASS scores across six dimensions."""

from __future__ import annotations
import argparse
import json
import logging
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import yaml

logging.basicConfig(
    level=logging.DEBUG if "--debug" in sys.argv else logging.WARNING,
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("validator")

SCORING = {
    "idempotency": {"start": 35, "pos": 8, "neg": -25},
    "security": {"start": 45, "pos": 12, "neg": -30},
    "module_selection": {"start": 55, "pos": 12, "neg": -25},
    "error_handling": {"start": 40, "pos": 15, "neg": -30},
    "structure": {"start": 65, "pos": 8, "neg": -20},
    "linting": {"start": 100, "pos": 0, "neg": -5},
}
THRESHOLDS = {
    "idempotency": 74,
    "security": 80,
    "module_selection": 81,
    "error_handling": 77,
    "structure": 91,
    "linting": 100,
}
IMPERATIVE = {"command", "shell", "raw", "script"}
DECLARATIVE = {
    "file",
    "copy",
    "template",
    "lineinfile",
    "blockinfile",
    "apt",
    "yum",
    "dnf",
    "pip",
    "package",
    "service",
    "systemd",
    "systemd_service",
    "user",
    "group",
}
STATE_MODULES = IMPERATIVE | DECLARATIVE
EXCUSED_CMDS = [
    r"pvecm\s+",
    r"pveceph\s+",
    r"pveum\s+",
    r"qm\s+",
    r"pct\s+",
    r"ceph\s+",
    r"ceph-volume\s+",
    r"microk8s\s+",
    r"kubectl\s+",
    r"helm\s+",
]
DEPRECATED = {
    "include",
    "synchronize",
    "docker",
    "ec2_facts",
    "ec2_vpc",
    "ecs_cluster",
    "ecs_service",
    "ecs_taskdefinition",
    "accelerate",
    "oc",
    "win_feature",
    "win_msi",
    "azure",
    "vsphere_guest",
    "digital_ocean",
    "rax",
    "gce",
    "s3",
    "docker_container",
    "docker_image",
    "docker_network",
    "docker_volume",
}
SECRET_PATS = [
    r"password:\s*['\"]?[^{'\"\s]+",
    r"secret:\s*['\"]?[^{'\"\s]+",
    r"api_key:\s*['\"]?[^{'\"\s]+",
    r"token:\s*['\"]?[^{'\"\s]+",
    r"private_key:\s*['\"]?[^{'\"\s]+",
]
DS_FP = [
    "secret_name",
    "secret_var_name",
    "infisical",
    "lookup(",
    "PROXMOX_",
    "sudo_nopasswd",
    "nopasswd",
    "NOPASSWD",
    "#",
    "{{",
    "defaults/main.yml",
    "msg:",
    "localhost",
    "127.0.0.1",
    "download.",
    "vault_",
]
META_KEYS = {
    "name",
    "when",
    "register",
    "loop",
    "loop_control",
    "notify",
    "tags",
    "vars",
    "environment",
    "become",
    "become_user",
    "delegate_to",
    "run_once",
    "changed_when",
    "failed_when",
    "ignore_errors",
    "no_log",
    "retries",
    "delay",
    "until",
    "block",
    "rescue",
    "always",
    "listen",
    "throttle",
}
MOCK_BAD = {
    "ceph_no_guards": (
        "- name: Bad OSD\n  command: /usr/bin/ceph-volume lvm create --data /dev/sdb\n"
        "- name: Bad shell\n  shell: /usr/bin/pveceph osd create /dev/sdc\n"
        "- name: Bad cmd\n  command: systemctl restart ceph.target\n"
        "- name: Bad raw\n  raw: echo hello\n- ansible.builtin.command: dd if=/dev/zero of=/dev/sdd\n"
        "- name: Bad script\n  script: /tmp/setup.sh\n"
    ),
    "secrets_exposed": (
        "- name: Bad password\n  user:\n    name: admin\n    password: SuperSecret123\n"
        "- name: Bad api_key\n  uri:\n    url: http://insecure.api/endpoint\n    headers:\n      api_key: sk-12345abcdef\n"
        "- name: Token exposed\n  shell: \"curl -H 'Auth: abc123' http://api.example.com\"\n"
        "- name: Good vault\n  debug:\n    msg: \"{{ lookup('vault', 'secret') }}\"\n"
    ),
    "deprecated_modules": (
        "- name: Deprecated include\n  include: other.yml\n"
        "- name: Deprecated synchronize\n  synchronize:\n    src: /tmp/foo\n    dest: /tmp/bar\n"
        "- name: Deprecated docker_container\n  docker_container:\n    name: test\n    image: nginx\n"
        "- name: Non-FQCN copy\n  copy:\n    src: file.txt\n    dest: /tmp/file.txt\n"
        "- name: Non-FQCN user\n  user:\n    name: testuser\n"
        "- name: Deprecated s3\n  s3:\n    bucket: mybucket\n    object: /myobject\n"
    ),
}


class ValidatorError(Exception):
    """Raised when validation encounters an unrecoverable error."""


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
        return {
            "pass": self.passed,
            "score": self.score,
            "issues": [str(i) for i in self.issues],
        }


@dataclass
class Result:
    role: str
    scenario: str
    timestamp: str
    dimensions: dict[str, DimResult]
    overall_pass: bool
    overall_score: int

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "scenario": self.scenario,
            "timestamp": self.timestamp,
            "dimensions": {k: v.to_dict() for k, v in self.dimensions.items()},
            "overall_pass": self.overall_pass,
            "overall_score": self.overall_score,
        }


def safe_read_text(path: Path) -> str | None:
    """Read file contents with explicit error handling. Returns None on failure."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        log.debug("File not found: %s", path)
        return None
    except PermissionError:
        log.warning("Permission denied: %s", path)
        return None
    except UnicodeDecodeError as e:
        log.warning("Encoding error %s: %s", path, e)
        return None
    except OSError as e:
        log.warning("OS error %s: %s", path, e)
        return None


def load_yaml(path: Path) -> list[dict] | None:
    """Load YAML file, returning list of documents or None on error."""
    content = safe_read_text(path)
    if content is None:
        return None
    if not content.strip():
        return []
    try:
        for doc in yaml.safe_load_all(content):
            if doc:
                return doc if isinstance(doc, list) else [doc]
        return []
    except yaml.YAMLError as e:
        log.warning("YAML error %s: %s", path, e)
        return None


def find_tasks(role: Path) -> list[Path]:
    """Find all task files in a role's tasks directory."""
    td = role / "tasks"
    if not td.exists():
        return []
    if not td.is_dir():
        log.warning("tasks is not a directory: %s", td)
        return []
    return list(td.glob("*.yml")) + list(td.glob("*.yaml"))


def line_map(path: Path) -> dict[int, int]:
    """Build mapping of task indices to line numbers."""
    content = safe_read_text(path)
    if content is None:
        return {}
    m, idx = {}, 0
    for i, ln in enumerate(content.split("\n"), 1):
        s = ln.lstrip()
        if (
            s.startswith("- name:")
            or s.startswith("- ansible.")
            or (s.startswith("- ") and ":" in s)
        ):
            m[idx] = i
            idx += 1
    return m


def get_module(task: dict) -> str:
    for k in task:
        if k not in META_KEYS:
            return k
    return ""


def _rel(tf: Path, role: Path) -> str:
    try:
        return str(tf.relative_to(role))
    except ValueError:
        return tf.name


def analyze_idempotency(role: Path) -> DimResult:
    """Analyze idempotency patterns in role tasks."""
    cfg, issues, pos, neg, imp_cnt, guarded = SCORING["idempotency"], [], 0, 0, 0, 0
    for tf in find_tasks(role):
        tasks, content = load_yaml(tf), safe_read_text(tf)
        if tasks is None or content is None:
            continue
        lm, rel = line_map(tf), _rel(tf, role)
        has_stat = "ansible.builtin.stat:" in content or "stat:" in content
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                continue
            ln, mod = lm.get(i, i + 1), get_module(t)
            mod_short = mod.split(".")[-1] if "." in mod else mod
            if mod_short not in STATE_MODULES:
                continue
            args = t.get(mod, {})
            if t.get("changed_when") is False:
                pos += cfg["pos"]
                guarded += 1
            elif "changed_when" in t:
                pos += cfg["pos"] // 2
                guarded += 1
            if isinstance(args, dict) and (args.get("creates") or args.get("removes")):
                pos += cfg["pos"] // 2
            if t.get("register") and t.get("when") and has_stat:
                pos += cfg["pos"] // 2
            if mod_short in IMPERATIVE:
                imp_cnt += 1
                cmd = str(
                    t.get(mod, args.get("cmd", "") if isinstance(args, dict) else "")
                )
                has_guard = "changed_when" in t or (t.get("when") and t.get("register"))
                excused = any(re.search(p, cmd) for p in EXCUSED_CMDS)
                if not has_guard and not excused:
                    neg += cfg["neg"]
                    issues.append(Issue(rel, ln, f"shell/cmd no guard: {cmd[:40]}"))
                elif not has_guard and excused:
                    neg += cfg["neg"] // 4
                    issues.append(Issue(rel, ln, "excused cmd missing changed_when"))
            elif mod_short in DECLARATIVE:
                pos += cfg["pos"] // 4
    base = cfg["start"] + 50 if imp_cnt == 0 else cfg["start"] + 30
    score = max(0, min(100, int(base + guarded * 5 + pos + neg)))
    return DimResult(score, score >= THRESHOLDS["idempotency"], issues)


def analyze_security(role: Path) -> DimResult:
    """Analyze security patterns and detect potential secrets."""
    cfg, issues, pos, neg, secrets_handled = SCORING["security"], [], 0, 0, 0
    for tf in find_tasks(role):
        tasks, content = load_yaml(tf), safe_read_text(tf)
        if tasks is None or content is None:
            continue
        rel = _rel(tf, role)
        for t in tasks:
            if isinstance(t, dict):
                if t.get("no_log") is True:
                    pos += cfg["pos"]
                    secrets_handled += 1
                tstr = str(t).lower()
                if "infisical" in tstr or "vault" in tstr or "lookup(" in tstr:
                    pos += cfg["pos"] // 2
                    secrets_handled += 1
        for ln_num, ln in enumerate(content.split("\n"), 1):
            stripped = ln.strip()
            if stripped.startswith("#") or not stripped:
                continue
            for p in SECRET_PATS:
                if (
                    re.search(p, ln, re.I)
                    and "{{" not in ln
                    and "lookup(" not in ln
                    and not any(fp in ln for fp in DS_FP)
                ):
                    neg += cfg["neg"]
                    issues.append(Issue(rel, ln_num, "hardcoded secret"))
                    break
            if (
                "http://" in ln
                and "https://" not in ln
                and not any(
                    e in ln
                    for e in [
                        "localhost",
                        "127.0.0.1",
                        "download.",
                        ".local",
                        "example",
                    ]
                )
            ):
                neg += cfg["neg"] // 2
                issues.append(Issue(rel, ln_num, "insecure http://"))
    try:
        result = subprocess.run(
            ["detect-secrets", "scan", str(role), "--all-files"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            try:
                scan_results = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                log.warning("detect-secrets invalid JSON: %s", e)
                scan_results = {}
            for fp, findings in scan_results.get("results", {}).items():
                fc_content = safe_read_text(Path(fp))
                fc = fc_content.split("\n") if fc_content else []
                for finding in findings:
                    ln = finding.get("line_number", 0)
                    lc = fc[ln - 1] if 0 < ln <= len(fc) else ""
                    if not any(pat in lc or pat in fp for pat in DS_FP):
                        neg += cfg["neg"]
                        issues.append(
                            Issue(fp, ln, f"detect-secrets: {finding.get('type', '?')}")
                        )
        else:
            log.debug(
                "detect-secrets exited %d: %s", result.returncode, result.stderr[:200]
            )
    except FileNotFoundError:
        log.debug("detect-secrets not installed")
    except subprocess.TimeoutExpired:
        log.warning("detect-secrets timed out")
        issues.append(Issue("validator", 0, "detect-secrets timeout"))
    except subprocess.SubprocessError as e:
        log.warning("detect-secrets error: %s", e)
    base = cfg["start"] + 40 if secrets_handled > 0 else cfg["start"] + 20
    return DimResult(
        max(0, min(100, base + pos + neg)),
        max(0, min(100, base + pos + neg)) >= THRESHOLDS["security"],
        issues,
    )


def analyze_modules(role: Path) -> DimResult:
    """Analyze module selection for FQCN usage and deprecated modules."""
    cfg, issues, fqcn, non_fqcn, dep, total = (
        SCORING["module_selection"],
        [],
        0,
        0,
        0,
        0,
    )
    skip_mods = {
        "block",
        "rescue",
        "always",
        "include_tasks",
        "import_tasks",
        "include_role",
        "import_role",
    }
    for tf in find_tasks(role):
        tasks = load_yaml(tf)
        if tasks is None:
            continue
        lm, rel = line_map(tf), _rel(tf, role)
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                continue
            mod = get_module(t)
            if not mod or mod in skip_mods:
                continue
            total += 1
            if "." in mod:
                fqcn += 1
            else:
                non_fqcn += 1
                issues.append(Issue(rel, lm.get(i, i + 1), f"non-FQCN: {mod}"))
            if mod in DEPRECATED or mod.split(".")[-1] in DEPRECATED:
                dep += 1
                issues.append(Issue(rel, lm.get(i, i + 1), f"deprecated: {mod}"))
    fqcn_ratio = (fqcn / total * 45) if total > 0 else 45
    score = max(
        0,
        min(
            100,
            int(
                cfg["start"]
                + fqcn_ratio
                - non_fqcn * (abs(cfg["neg"]) // 2)
                - dep * abs(cfg["neg"])
            ),
        ),
    )
    return DimResult(score, score >= THRESHOLDS["module_selection"], issues)


def analyze_errors(role: Path) -> DimResult:
    """Analyze error handling patterns in role tasks."""
    cfg, issues, pos, neg, blocks, rescues, failed_whens, cnt = (
        SCORING["error_handling"],
        [],
        0,
        0,
        0,
        0,
        0,
        0,
    )
    for tf in find_tasks(role):
        tasks = load_yaml(tf)
        if tasks is None:
            continue
        lm, rel = line_map(tf), _rel(tf, role)
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                continue
            cnt += 1
            if "block" in t:
                blocks += 1
                if "rescue" in t:
                    rescues += 1
                    pos += cfg["pos"]
                else:
                    neg += cfg["neg"] // 3
                    issues.append(Issue(rel, lm.get(i, i + 1), "block without rescue"))
            if "failed_when" in t:
                failed_whens += 1
                pos += cfg["pos"] // 2
            if t.get("ignore_errors") is True and not t.get("register"):
                neg += cfg["neg"]
                issues.append(
                    Issue(rel, lm.get(i, i + 1), "ignore_errors w/o register")
                )
    if blocks > 0 and rescues / blocks < 0.5:
        neg += cfg["neg"]
    base = 35 if (blocks > 0 and rescues > 0) or failed_whens > 2 else 20
    score = max(0, min(100, cfg["start"] + base + pos + neg)) if cnt > 0 else 100
    return DimResult(score, score >= THRESHOLDS["error_handling"], issues)


def analyze_structure(role: Path) -> DimResult:
    """Analyze role structure for best practices."""
    cfg, issues, pos, neg = SCORING["structure"], [], 0, 0
    if (role / "defaults" / "main.yml").exists():
        pos += cfg["pos"]
    if (role / "handlers").exists() and list((role / "handlers").glob("*.yml")):
        pos += cfg["pos"]
    if (role / "meta" / "main.yml").exists():
        pos += cfg["pos"]
    task_files = find_tasks(role)
    named, unnamed, tfc = 0, 0, len(task_files)
    depth = sum(
        1
        for tf in task_files
        if "/" in str(tf.relative_to(role / "tasks"))
        if (role / "tasks").exists()
    )
    for tf in task_files:
        tasks = load_yaml(tf)
        if tasks is None:
            continue
        lm, rel = line_map(tf), _rel(tf, role)
        for i, t in enumerate(tasks):
            if not isinstance(t, dict):
                continue
            if t.get("name"):
                named += 1
            elif get_module(t) not in ("block", "rescue", "always"):
                unnamed += 1
                neg += cfg["neg"]
                issues.append(Issue(rel, lm.get(i, i + 1), "unnamed task"))
    if tfc > 10:
        neg += (tfc - 10) * (abs(cfg["neg"]) // 2)
        issues.append(Issue("role", 0, f"{tfc} task files (>10)"))
    if depth > 1:
        neg += depth * abs(cfg["neg"])
    total = named + unnamed
    score = max(
        0,
        min(
            100,
            int(cfg["start"] + (named / total * 25 if total > 0 else 25) + pos + neg),
        ),
    )
    return DimResult(score, score >= THRESHOLDS["structure"], issues)


def analyze_linting(
    role: Path, cfg_path: Path | None = None, policy_skip: list[str] | None = None
) -> DimResult:
    """Run ansible-lint and analyze results."""
    if cfg_path is None:
        p = role
        while p != p.parent:
            for n in [".ansible-lint", ".ansible-lint.yml"]:
                if (p / n).exists():
                    cfg_path = p / n
                    break
            if cfg_path:
                break
            p = p.parent
    cmd = (
        ["ansible-lint", str(role)]
        + (["-c", str(cfg_path)] if cfg_path else [])
        + (["-x", ",".join(policy_skip)] if policy_skip else [])
    )
    try:
        cwd = role.parent.parent if "roles" in str(role) else role.parent
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60, cwd=cwd
        )
        violations = len(
            [
                ln
                for ln in result.stdout.split("\n")
                if ": " in ln and not ln.startswith(" ")
            ]
        )
        warnings = len(
            [ln for ln in result.stdout.split("\n") if "warning" in ln.lower()]
        )
        if result.returncode == 0 or violations == 0:
            return DimResult(100 - warnings * SCORING["linting"]["neg"], True, [])
        return DimResult(
            max(0, 100 - violations * 5 - warnings * 2),
            False,
            [Issue("lint", 0, f"{violations} violations, {warnings} warnings")],
        )
    except FileNotFoundError:
        log.warning("ansible-lint not installed")
        return DimResult(
            0, False, [Issue("validator", 0, "ansible-lint not installed")]
        )
    except subprocess.TimeoutExpired:
        log.warning("ansible-lint timed out for: %s", role)
        return DimResult(50, False, [Issue("validator", 0, "lint timeout (60s)")])
    except subprocess.SubprocessError as e:
        log.warning("ansible-lint error: %s", e)
        return DimResult(0, False, [Issue("validator", 0, f"lint error: {e}")])


def validate(
    role: Path,
    cfg: Path | None = None,
    policy_skip: list[str] | None = None,
    raw: bool = False,
) -> Result:
    """Run full validation across all dimensions."""
    role_path = str(role.resolve())
    if any(
        p in role_path
        for p in [".ansible/roles", "ansible_collections", ".cache/ansible-compat"]
    ):
        return Result(
            role.name,
            role.name.replace("_", "-"),
            datetime.now(timezone.utc).isoformat(),
            {},
            True,
            100,
        )
    dims = {
        "idempotency": analyze_idempotency(role),
        "security": analyze_security(role),
        "module_selection": analyze_modules(role),
        "error_handling": analyze_errors(role),
        "structure": analyze_structure(role),
        "linting": analyze_linting(role, None if raw else cfg, policy_skip),
    }
    overall = sum(d.score for d in dims.values()) // len(dims)
    return Result(
        role.name,
        role.name.replace("_", "-"),
        datetime.now(timezone.utc).isoformat(),
        dims,
        all(d.passed for d in dims.values()),
        overall,
    )


def validate_mock(name: str) -> Result:
    """Validate a mock bad playbook for calibration testing."""
    if name not in MOCK_BAD:
        log.warning("Unknown mock: %s", name)
        return Result(name, name, datetime.now(timezone.utc).isoformat(), {}, False, 0)
    with tempfile.TemporaryDirectory() as td:
        role = Path(td) / name
        (role / "tasks").mkdir(parents=True)
        (role / "tasks" / "main.yml").write_text(MOCK_BAD[name])
        dims = {
            "idempotency": analyze_idempotency(role),
            "security": analyze_security(role),
            "module_selection": analyze_modules(role),
            "error_handling": analyze_errors(role),
            "structure": analyze_structure(role),
            "linting": DimResult(50, False, [Issue("mock", 0, "lint skipped")]),
        }
        return Result(
            name,
            name,
            datetime.now(timezone.utc).isoformat(),
            dims,
            all(d.passed for d in dims.values()),
            sum(d.score for d in dims.values()) // len(dims),
        )


def compare(base: Path, curr: Path) -> dict:
    """Compare two validation result JSON files."""
    try:
        base_content, curr_content = safe_read_text(base), safe_read_text(curr)
        if base_content is None:
            raise ValidatorError(f"Cannot read baseline: {base}")
        if curr_content is None:
            raise ValidatorError(f"Cannot read current: {curr}")
        b, c = json.loads(base_content), json.loads(curr_content)
    except json.JSONDecodeError as e:
        raise ValidatorError(f"Invalid JSON: {e}") from e
    return {
        "role": c.get("role"),
        "dimension_deltas": {
            d: {
                "baseline": b["dimensions"][d]["score"],
                "current": c["dimensions"][d]["score"],
                "delta": c["dimensions"][d]["score"] - b["dimensions"][d]["score"],
            }
            for d in b.get("dimensions", {})
            if d in c.get("dimensions", {})
        },
        "overall_delta": c.get("overall_score", 0) - b.get("overall_score", 0),
    }


def fmt_table(r: Result) -> str:
    """Format validation result as ASCII table."""
    lines = [
        f"\nValidation Results: {r.role}",
        "=" * 60,
        f"{'Dimension':<20} {'Score':>6} {'Pass':>6} {'Issues':>8}",
        "-" * 60,
    ]
    lines += [
        f"{d:<20} {res.score:>5}% {'PASS' if res.passed else 'FAIL':>6} {len(res.issues):>8}"
        for d, res in r.dimensions.items()
    ]
    lines += [
        "-" * 60,
        f"{'OVERALL':<20} {r.overall_score:>5}% {'PASS' if r.overall_pass else 'FAIL':>6}",
        "=" * 60,
    ]
    issues = [f"  [{d}] {i}" for d, res in r.dimensions.items() for i in res.issues[:3]]
    return "\n".join(lines + (["\nTop Issues:"] + issues[:10] if issues else []))


def get_roles_dir() -> Path | None:
    rd = Path(__file__).parent.parent / "ansible" / "roles"
    return rd if rd.exists() else None


def main() -> int:
    """Main entry point for CLI."""
    p = argparse.ArgumentParser(description="Ansible Role Quality Validator")
    a = p.add_argument
    a("--role", "--playbook", type=Path, dest="role")
    a("--scenario", type=str)
    a("--dimension", choices=list(THRESHOLDS.keys()))
    a("--all-roles", action="store_true")
    a("--output", choices=["json", "table"], default="table")
    a("--lint-config", type=Path)
    a("--raw", action="store_true")
    a("--policy-skip", type=str)
    a("--compare", nargs=2, metavar=("BASE", "CURR"))
    a("--calibrate", action="store_true")
    a("--mock", type=str, choices=list(MOCK_BAD.keys()))
    a("--debug", action="store_true")
    args = p.parse_args()
    pskip = args.policy_skip.split(",") if args.policy_skip else None
    if args.compare:
        try:
            print(
                json.dumps(
                    compare(Path(args.compare[0]), Path(args.compare[1])), indent=2
                )
            )
            return 0
        except ValidatorError as e:
            log.error("%s", e)
            return 2
    if args.mock:
        r = validate_mock(args.mock)
        print(
            json.dumps(r.to_dict(), indent=2) if args.output == "json" else fmt_table(r)
        )
        return 0 if r.overall_pass else 1
    if args.calibrate or args.all_roles:
        rd = get_roles_dir()
        if not rd:
            log.error("Roles directory not found")
            return 2
        results = [
            validate(d, args.lint_config, pskip, args.raw)
            for d in sorted(rd.iterdir())
            if d.is_dir() and not d.name.startswith(".")
        ]
        if args.calibrate:
            print("Calibration: Reference roles\n" + "-" * 50)
            for r in results:
                print(f"  {r.role:<25} {r.overall_score:>3}%")
            print("\nDimension Averages:")
            for d in THRESHOLDS:
                scores = [r.dimensions[d].score for r in results if d in r.dimensions]
                if scores:
                    avg = sum(scores) / len(scores)
                    print(
                        f"  {d:<20} {avg:>5.1f}% (threshold: {THRESHOLDS[d]}%) [{'OK' if avg >= THRESHOLDS[d] * 0.9 else 'LOW'}]"
                    )
            print("\nMock Bad Playbooks:\n" + "-" * 50)
            for mn in MOCK_BAD:
                mr = validate_mock(mn)
                print(f"  {mn:<25} {mr.overall_score:>3}% (target: <50%)")
            return 0
        print(
            json.dumps([r.to_dict() for r in results], indent=2)
            if args.output == "json"
            else "\n".join(fmt_table(r) for r in results)
        )
        return 0 if all(r.overall_pass for r in results) else 1
    if args.scenario and not args.role:
        rd = get_roles_dir()
        if rd:
            args.role = rd / {
                "proxmox-cluster": "proxmox_cluster",
                "ceph-storage": "proxmox_ceph",
                "proxmox-access": "proxmox_access",
                "proxmox-network": "proxmox_network",
            }.get(args.scenario, args.scenario.replace("-", "_"))
    if not args.role:
        p.print_help()
        return 2
    if not args.role.exists():
        log.error("Role path does not exist: %s", args.role)
        return 2
    if not args.role.is_dir():
        log.error("Role path is not a directory: %s", args.role)
        return 2
    if args.dimension:
        analyzers = {
            "idempotency": analyze_idempotency,
            "security": analyze_security,
            "module_selection": analyze_modules,
            "error_handling": analyze_errors,
            "structure": analyze_structure,
            "linting": lambda r: analyze_linting(r, args.lint_config, pskip),
        }
        res = analyzers[args.dimension](args.role)
        print(
            json.dumps({args.dimension: res.to_dict()}, indent=2)
            if args.output == "json"
            else f"\n{args.dimension}: {res.score}% ({'PASS' if res.passed else 'FAIL'})\n"
            + "\n".join(f"  - {i}" for i in res.issues)
        )
        return 0 if res.passed else 1
    r = validate(args.role, args.lint_config, pskip, args.raw)
    print(json.dumps(r.to_dict(), indent=2) if args.output == "json" else fmt_table(r))
    return 0 if r.overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
