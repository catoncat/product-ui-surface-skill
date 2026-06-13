#!/usr/bin/env python3
"""Scan visible UI text for product-brief leakage and explanatory phrases."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path


DEFAULT_PATTERNS = [
    "帮助用户",
    "提升效率",
    "高效管理",
    "可控",
    "低干扰",
    "这个界面",
    "本界面",
    "本功能",
    "旨在",
    "用于",
    "用户可以",
    "你可以",
    "您可以",
    "这里可以",
    "系统会",
    "系统将",
    "平台会",
    "点击按钮",
    "打开菜单",
    "选择下拉框",
    "agentic workflow",
    "manage capabilities",
    "designed to",
    "this interface",
    "this feature",
    "helps users",
    "allows users to",
]


def read_terms_file(raw_path: str) -> list[str]:
    path = Path(raw_path)
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    return terms


def parse_contract_terms(raw_path: str) -> list[str]:
    """Extract bullet terms from a markdown `forbidden_brief_terms:` section."""
    path = Path(raw_path)
    terms = []
    in_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "forbidden_brief_terms:":
            in_section = True
            continue
        if not in_section:
            continue
        if not stripped:
            continue
        if stripped.startswith("- "):
            term = stripped[2:].strip()
            if term:
                terms.append(term)
            continue
        if re.match(r"^[A-Za-z0-9_-]+:", stripped):
            break
    return terms


def unique_terms(terms: list[str]) -> list[str]:
    seen = set()
    unique = []
    for term in terms:
        key = term.casefold()
        if key not in seen:
            seen.add(key)
            unique.append(term)
    return unique


def load_forbidden(
    paths: list[str],
    inline: list[str],
    contracts: list[str],
    include_defaults: bool,
    allowed_terms: list[str],
) -> list[str]:
    terms = list(DEFAULT_PATTERNS) if include_defaults else []
    terms.extend(inline)
    for raw_path in paths:
        terms.extend(read_terms_file(raw_path))
    for raw_path in contracts:
        terms.extend(parse_contract_terms(raw_path))

    allowed = {term.casefold() for term in allowed_terms}
    return [term for term in unique_terms(terms) if term.casefold() not in allowed]


def excluded(path: Path, patterns: list[str]) -> bool:
    value = str(path)
    return any(pattern in value or fnmatch.fnmatch(value, pattern) or fnmatch.fnmatch(path.name, pattern) for pattern in patterns)


def iter_inputs(paths: list[str], exclude_patterns: list[str]) -> list[tuple[str, str]]:
    if not paths:
        return [("<stdin>", sys.stdin.read())]
    chunks = []
    for raw_path in paths:
        path = Path(raw_path)
        if excluded(path, exclude_patterns):
            continue
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if excluded(child, exclude_patterns):
                    continue
                if child.is_file() and child.suffix.lower() in {
                    ".txt",
                    ".md",
                    ".html",
                    ".json",
                    ".ts",
                    ".tsx",
                    ".js",
                    ".jsx",
                    ".vue",
                    ".svelte",
                }:
                    chunks.append((str(child), child.read_text(encoding="utf-8", errors="ignore")))
        else:
            chunks.append((str(path), path.read_text(encoding="utf-8", errors="ignore")))
    return chunks


def line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_newline = text.rfind("\n", 0, index)
    col = index + 1 if last_newline == -1 else index - last_newline
    return line, col


def scan(name: str, text: str, patterns: list[str]) -> list[dict[str, object]]:
    findings = []
    for pattern in patterns:
        regex = re.compile(re.escape(pattern), re.IGNORECASE)
        for match in regex.finditer(text):
            line, col = line_col(text, match.start())
            excerpt_start = max(0, match.start() - 36)
            excerpt_end = min(len(text), match.end() + 36)
            findings.append(
                {
                    "file": name,
                    "line": line,
                    "column": col,
                    "term": pattern,
                    "excerpt": " ".join(text[excerpt_start:excerpt_end].split()),
                }
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan UI-visible text or UI source files for brief leakage terms."
    )
    parser.add_argument("paths", nargs="*", help="Files or directories to scan. Reads stdin when omitted.")
    parser.add_argument(
        "--forbidden",
        action="append",
        default=[],
        help="File with one additional forbidden term per line.",
    )
    parser.add_argument(
        "--contract",
        action="append",
        default=[],
        help="Surface language contract markdown file. Reads forbidden_brief_terms bullets.",
    )
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        help="Additional forbidden term. Can be provided multiple times.",
    )
    parser.add_argument(
        "--allow",
        action="append",
        default=[],
        help="Allowed term to suppress from findings. Can be provided multiple times.",
    )
    parser.add_argument(
        "--allow-file",
        action="append",
        default=[],
        help="File with one allowed term per line.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Skip paths matching this glob or substring. Can be provided multiple times.",
    )
    parser.add_argument(
        "--no-defaults",
        action="store_true",
        help="Disable built-in brief-leak patterns and use only --term, --forbidden, or --contract terms.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    allowed_terms = list(args.allow)
    for raw_path in args.allow_file:
        allowed_terms.extend(read_terms_file(raw_path))

    patterns = load_forbidden(
        args.forbidden,
        args.term,
        args.contract,
        include_defaults=not args.no_defaults,
        allowed_terms=allowed_terms,
    )
    findings = []
    for name, text in iter_inputs(args.paths, args.exclude):
        findings.extend(scan(name, text, patterns))

    if args.json:
        print(json.dumps({"ok": not findings, "findings": findings}, ensure_ascii=False, indent=2))
    elif findings:
        for item in findings:
            print(
                f"{item['file']}:{item['line']}:{item['column']} "
                f"brief-leak term={item['term']!r} excerpt={item['excerpt']!r}"
            )
    else:
        print("No brief-leak terms found.")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
