#!/usr/bin/env python3
"""Scan visible UI text for product-brief leakage and explanatory phrases."""

from __future__ import annotations

import argparse
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


def load_forbidden(paths: list[str], inline: list[str]) -> list[str]:
    terms = list(DEFAULT_PATTERNS)
    terms.extend(inline)
    for raw_path in paths:
        path = Path(raw_path)
        for line in path.read_text(encoding="utf-8").splitlines():
            term = line.strip()
            if term and not term.startswith("#"):
                terms.append(term)
    seen = set()
    unique = []
    for term in terms:
        key = term.casefold()
        if key not in seen:
            seen.add(key)
            unique.append(term)
    return unique


def iter_inputs(paths: list[str]) -> list[tuple[str, str]]:
    if not paths:
        return [("<stdin>", sys.stdin.read())]
    chunks = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
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
        "--term",
        action="append",
        default=[],
        help="Additional forbidden term. Can be provided multiple times.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    patterns = load_forbidden(args.forbidden, args.term)
    findings = []
    for name, text in iter_inputs(args.paths):
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
