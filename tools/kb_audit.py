#!/usr/bin/env python3
"""Lightweight structural audit for the FDE Obsidian knowledge base.

The checker is dependency-free and intentionally conservative: it reports
problems without rewriting notes.  Run it from the repository root.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


REQUIRED_FIELDS = {
    "type",
    "domain",
    "layer",
    "canonical",
    "status",
    "created",
    "updated",
    "sources",
}
ALLOWED_VALUES = {
    "type": {"concept", "guide", "tutorial", "reference", "case-study", "moc", "archive"},
    "domain": {
        "concept",
        "language",
        "frontend",
        "backend",
        "data",
        "ai",
        "automation",
        "infra",
        "integration",
        "engineering",
        "topic",
    },
    "layer": {"foundation", "advanced", "implementation", "case-study"},
    "canonical": {"true", "false"},
    "status": {"active", "evolving", "archive"},
}
EXEMPT_FILES = {"README.md"}
IGNORED_LINK_TARGETS = {"wikilinks", "双链", "链接", "笔记名"}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def vault_root(root: Path) -> Path:
    return root / "FDE技术栈知识库"


def markdown_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in {".git", ".obsidian", "tools"} for part in path.parts):
            continue
        result.append(path)
    return sorted(result)


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        return {}, text
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if item:
            values[item.group(1)] = item.group(2).strip()
    return values, text[match.end() :]


def without_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def links(text: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(r"\[\[([^|\]#]+)(?:\|[^\]]+)?\]\]", without_fences(text))
    ]


def normalize(text: str) -> str:
    text = without_fences(text)
    text = re.sub(r"^---.*?---", " ", text, flags=re.S)
    text = re.sub(r"\[\[([^|\]#]+)(?:\|[^\]]+)?\]\]", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)|\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"[#>*_`~|—–·•:：,，。！？!?；;（）()\[\]{}\"“”'`]", "", text)
    return re.sub(r"\s+", "", text).lower()


def shingles(text: str, size: int = 3) -> set[str]:
    return {text[index : index + size] for index in range(max(0, len(text) - size + 1))}


def duplicate_paragraphs(texts: dict[Path, str]) -> list[dict[str, object]]:
    occurrences: dict[str, list[str]] = defaultdict(list)
    for path, text in texts.items():
        for paragraph in re.split(r"\n\s*\n", without_fences(text)):
            value = normalize(paragraph)
            if len(value) >= 80:
                occurrences[value].append(str(path))
    duplicates = []
    for value, paths in occurrences.items():
        unique = sorted(set(paths))
        if len(unique) > 1:
            duplicates.append({"chars": len(value), "files": unique})
    return sorted(duplicates, key=lambda item: (-len(item["files"]), -item["chars"]))


def similar_pairs(texts: dict[Path, str], threshold: float = 0.18) -> list[dict[str, object]]:
    values = {path: shingles(normalize(text)) for path, text in texts.items()}
    result = []
    for left, right in itertools.combinations(sorted(values), 2):
        if len(values[left]) < 100 or len(values[right]) < 100:
            continue
        union = values[left] | values[right]
        if not union:
            continue
        score = len(values[left] & values[right]) / len(union)
        if score >= threshold:
            result.append({"score": round(score, 3), "files": [str(left), str(right)]})
    return sorted(result, key=lambda item: (-item["score"], item["files"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--strict", action="store_true", help="return non-zero when issues remain")
    args = parser.parse_args()

    root = repo_root()
    vault = vault_root(root)
    files = markdown_files(root)
    texts = {path: path.read_text(encoding="utf-8") for path in files}
    metadata = {
        path: parse_frontmatter(text)[0]
        for path, text in texts.items()
        if path.name not in EXEMPT_FILES
    }

    basenames: dict[str, list[Path]] = defaultdict(list)
    aliases: dict[str, list[Path]] = defaultdict(list)
    for path, fields in metadata.items():
        basenames[path.stem].append(path)
        alias_value = fields.get("aliases", "")
        for alias in re.findall(r"[A-Za-z0-9_./+\-]+|[\u4e00-\u9fff]+", alias_value):
            aliases[alias].append(path)

    missing_fields: dict[str, list[str]] = defaultdict(list)
    invalid_values: dict[str, list[str]] = defaultdict(list)
    for path, fields in metadata.items():
        missing = sorted(REQUIRED_FIELDS - set(fields))
        for field in missing:
            missing_fields[field].append(rel(path, root))
        for field, allowed in ALLOWED_VALUES.items():
            value = fields.get(field)
            if value and value not in allowed:
                invalid_values[field].append(f"{rel(path, root)}={value}")

    unresolved: Counter[str] = Counter()
    ambiguous: dict[str, list[str]] = {}
    incoming: Counter[Path] = Counter()
    link_sources: dict[str, list[str]] = defaultdict(list)
    for path, text in texts.items():
        if path.name in EXEMPT_FILES:
            continue
        for target in links(text):
            if target in IGNORED_LINK_TARGETS:
                continue
            candidates = basenames.get(target, []) or aliases.get(target, [])
            if not candidates:
                unresolved[target] += 1
                link_sources[target].append(f"{rel(path, root)}")
            elif len(candidates) > 1:
                ambiguous[target] = [rel(candidate, root) for candidate in candidates]
            else:
                incoming[candidates[0]] += 1

    moc = vault / "FDE 技术栈 MOC.md"
    moc_targets = set(links(texts[moc])) if moc in texts else set()
    active_files = {
        path
        for path, fields in metadata.items()
        if fields.get("status") in {"active", "evolving"} and path != moc
    }
    moc_by_name = {path.stem: path for path in active_files}
    moc_missing = sorted(rel(path, root) for path in active_files if path.stem not in moc_targets)

    hashes: dict[str, list[str]] = defaultdict(list)
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes[digest].append(rel(path, root))
    duplicate_files = [paths for paths in hashes.values() if len(paths) > 1]

    orphans = sorted(
        rel(path, root)
        for path in active_files
        if incoming[path] == 0 and path.stem not in {"README", "FDE（Forward Deployed Engineer）技术栈完整指南"}
    )
    canonical_groups: Counter[str] = Counter()
    canonical_without_group: list[str] = []
    for path, fields in metadata.items():
        if fields.get("canonical") == "true" and fields.get("status") in {"active", "evolving"}:
            group = fields.get("canonical_group", "").strip()
            if not group:
                canonical_without_group.append(rel(path, root))
            else:
                canonical_groups[group] += 1
    canonical_collisions = {group: count for group, count in canonical_groups.items() if count > 1}

    report = {
        "files": len(files),
        "vault_files": sum(1 for path in files if path.is_relative_to(vault)),
        "missing_frontmatter": [rel(path, root) for path, fields in metadata.items() if not fields],
        "missing_fields": dict(missing_fields),
        "invalid_values": dict(invalid_values),
        "unresolved_links": dict(unresolved),
        "ambiguous_links": ambiguous,
        "moc_missing_active": moc_missing,
        "orphans": orphans,
        "duplicate_files": duplicate_files,
        "duplicate_paragraphs": duplicate_paragraphs(texts),
        "similar_pairs": similar_pairs(texts),
        "canonical_collisions": canonical_collisions,
        "canonical_without_group": canonical_without_group,
    }

    errors = (
        report["missing_frontmatter"]
        or report["missing_fields"]
        or report["invalid_values"]
        or report["unresolved_links"]
        or report["ambiguous_links"]
        or report["moc_missing_active"]
        or report["duplicate_files"]
        or report["canonical_collisions"]
        or report["canonical_without_group"]
    )

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Markdown files: {report['files']} (vault: {report['vault_files']})")
        print(f"Unresolved links: {sum(unresolved.values())}")
        print(f"MOC gaps: {len(moc_missing)}")
        print(f"Orphans: {len(orphans)}")
        print(f"Duplicate files: {len(duplicate_files)}")
        print(f"Duplicate paragraphs: {len(report['duplicate_paragraphs'])}")
        print(f"Similar pairs >= 0.18: {len(report['similar_pairs'])}")
        if errors:
            print("\nIssues:")
            for key, value in report.items():
                if value and key not in {"files", "vault_files", "duplicate_paragraphs", "similar_pairs", "orphans"}:
                    print(f"- {key}: {value}")
        else:
            print("\nAudit passed.")

    return 1 if args.strict and errors else 0


if __name__ == "__main__":
    sys.exit(main())
