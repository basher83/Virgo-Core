"""Validate this wiki's structure and pinned source hashes; never run infrastructure."""
import hashlib
import json
from pathlib import Path
import re
import sys


def validate(wiki):
    root = wiki.parent
    errors = []
    administrative = {"SCHEMA", "index", "log"}
    documents = {p.stem: p for p in wiki.glob("*.md")}
    pages = {k: p for k, p in documents.items() if k not in administrative}
    inbound = {k: 0 for k in pages}
    index = (wiki / "index.md").read_text()
    manifest = json.loads((wiki / "raw/source-manifest.json").read_text())
    source_paths = {entry["path"] for entry in manifest["sources"]}
    required = {"title", "created", "updated", "type", "tags", "sources", "confidence", "source_revision"}
    for name, path in documents.items():
        text = path.read_text()
        links = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text)
        for target in links:
            if target not in documents:
                errors.append(f"{name}: broken wikilink {target}")
            elif target in inbound and name != target:
                inbound[target] += 1
        for target in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^)]+)\)", text):
            if "://" not in target and not target.startswith("#"):
                local = target.split("#", 1)[0]
                if not (path.parent / local).exists():
                    errors.append(f"{name}: broken local link {target}")
        if name in administrative:
            continue
        if len(text.splitlines()) > 200:
            errors.append(f"{name}: exceeds 200 lines")
        if len(set(links) - {name}) < 2:
            errors.append(f"{name}: fewer than two outbound wikilinks")
        if f"[[{name}]]" not in index:
            errors.append(f"{name}: missing from index")
        try:
            if not text.startswith("---\n"):
                raise ValueError("missing frontmatter")
            metadata = {}
            for line in text.split("---", 2)[1].strip().splitlines():
                key, value = line.split(":", 1)
                metadata[key] = json.loads(value.strip())
            if required - metadata.keys():
                raise ValueError(f"missing fields {required - metadata.keys()}")
            if set(metadata["tags"]) - {"virgo-core"}:
                raise ValueError("unknown tags")
            if metadata["type"] not in {"concept", "summary", "comparison", "query", "entity"}:
                raise ValueError("unknown type")
            if metadata["source_revision"] != manifest["revision"]:
                raise ValueError("revision mismatch")
            if not metadata["sources"] or set(metadata["sources"]) - source_paths:
                raise ValueError("unmanifested or missing sources")
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            errors.append(f"{name}: metadata {exc}")
    for name, count in inbound.items():
        if count == 0:
            errors.append(f"{name}: orphan")
    declared = re.search(r"\*\*Content pages:\*\* (\d+)", index)
    if not declared or int(declared.group(1)) != len(pages):
        errors.append("index: page count mismatch")
    for entry in manifest["sources"]:
        source = root / entry["path"]
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != entry["sha256"]:
            errors.append(f"source drift: {entry['path']}")
    return errors, len(pages), len(source_paths)


if __name__ == "__main__":
    errors, page_count, source_count = validate(Path(__file__).resolve().parent)
    for error in errors:
        print(error)
    print(f"{page_count} content pages; {source_count} pinned sources; {len(errors)} errors")
    sys.exit(bool(errors))
