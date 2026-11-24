"""Audit all 28 source question files without changing question databases.

Run from the repository root:
    python3 tools/audit_questions.py

The report covers source-file integrity only. It is NOT a comparison with
the latest proprietary 1C certification question bank.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PARTS = (
    "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen"
)
QUESTION_NUMBER = re.compile(r"^\s*(\d+)\.(\d+)\s+(.+)$")
CHOICES = "abcdef"


def parse_section(exam: str, number: int, slug: str) -> dict:
    path = ROOT / "questions" / exam / f"part_{slug}.txt"
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    findings = []
    entries = []

    if len(lines) % 9:
        findings.append({
            "type": "invalid_line_count",
            "detail": f"{len(lines)} nontrailing lines: expected a multiple of nine"
        })

    for offset in range(0, len(lines), 9):
        block = lines[offset:offset + 9]
        if len(block) != 9:
            break
        match = QUESTION_NUMBER.match(block[0])
        if not match:
            findings.append({
                "type": "invalid_question_heading",
                "line": offset + 1,
                "detail": block[0][:100]
            })
            continue

        chapter, index = int(match[1]), int(match[2])
        answer = block[7].strip().lower()
        variants = []
        for pos, line in enumerate(block[1:7], 1):
            text = line.strip()
            if text:
                if not text.startswith(f"{pos}."):
                    findings.append({
                        "type": "malformed_option_number",
                        "question": f"{chapter}.{index}",
                        "line": offset + pos + 1
                    })
                variants.append(text.split(".", 1)[-1].strip())
            else:
                variants.append("")

        if chapter != number:
            findings.append({
                "type": "wrong_chapter_number",
                "question": f"{chapter}.{index}",
                "expected": number
            })
        if answer not in CHOICES:
            findings.append({
                "type": "invalid_answer_letter",
                "question": f"{chapter}.{index}",
                "answer": answer
            })
        elif not variants[CHOICES.index(answer)]:
            findings.append({
                "type": "empty_correct_option",
                "question": f"{chapter}.{index}",
                "answer": answer
            })
        entries.append({"index": index, "question": match[3], "answer": answer})

    counts = Counter(entry["index"] for entry in entries)
    for index, occurrences in counts.items():
        if occurrences > 1:
            findings.append({
                "type": "duplicate_number",
                "question": f"{number}.{index}",
                "occurrences": occurrences
            })
    if entries:
        highest = max(item["index"] for item in entries)
        for index in range(1, highest + 1):
            if index not in counts:
                findings.append({"type": "missing_number", "question": f"{number}.{index}"})

    return {
        "exam": exam,
        "section": number,
        "file": str(path.relative_to(ROOT)),
        "question_count": len(entries),
        "findings": findings
    }


def audit() -> dict:
    sections = [
        parse_section(exam, n, slug)
        for exam in ("prof", "erp")
        for n, slug in enumerate(PARTS, 1)
    ]
    return {
        "scope": "repository_source_files_only",
        "totals": {
            exam: sum(x["question_count"] for x in sections if x["exam"] == exam)
            for exam in ("prof", "erp")
        },
        "issues": [
            {"exam": x["exam"], "section": x["section"], **issue}
            for x in sections for issue in x["findings"]
        ],
        "sections": sections
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
