"""Check how many of the repository's exam questions have a matching explanation.

Run: python3 tools/audit_explanations.py
Read-only: does not import Flask or alter the SQLite databases.
"""
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "databases" / "explanation_seeds.json"
PARTS = ("one", "two", "three", "four", "five", "six", "seven",
         "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen")
OPTIONS = "abcdef"


def normalize(text):
    return " ".join(str(text or "").split()).casefold()


def audit():
    seeds = json.loads(SEEDS.read_text(encoding="utf-8"))
    by_key = {(item["exam"], normalize(item["question"]),
               normalize(item["answer"]), normalize(item["answer_text"]))
              for item in seeds}
    found = set()
    totals = {"prof": {"questions": 0, "explained": 0},
              "erp": {"questions": 0, "explained": 0}}
    for exam in totals:
        for number, part in enumerate(PARTS, 1):
            file = ROOT / "questions" / exam / f"part_{part}.txt"
            lines = file.read_text(encoding="utf-8-sig").splitlines()
            while lines and not lines[-1].strip():
                lines.pop()
            for i in range(0, len(lines), 9):
                block = lines[i:i + 9]
                if len(block) != 9:
                    continue
                header = re.match(r"^\s*\d+\.\d+\s+(.+)", block[0])
                if not header:
                    continue
                answer = block[7].strip().lower()
                if answer not in OPTIONS:
                    continue
                text = block[1 + OPTIONS.index(answer)]
                text = re.sub(r"^\s*\d+\.\s*", "", text)
                key = (exam, normalize(header.group(1)), normalize(answer), normalize(text))
                totals[exam]["questions"] += 1
                if key in by_key:
                    totals[exam]["explained"] += 1
                    found.add(key)
    database_stats = {"verified_or_curated": 0, "unverified_drafts": 0}
    database_path = ROOT / "explanations.db"
    if database_path.is_file():
        connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
        try:
            found = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='explanations'"
            ).fetchone()
            if found:
                for source_type, count in connection.execute(
                    "SELECT source_type, COUNT(*) FROM explanations GROUP BY source_type"
                ):
                    kind = ("unverified_drafts"
                            if source_type.startswith("Предварительный разбор")
                            else "verified_or_curated")
                    database_stats[kind] += count
        finally:
            connection.close()
    return {
        "per_exam": totals,
        "total_questions": sum(x["questions"] for x in totals.values()),
        "covered_questions": sum(x["explained"] for x in totals.values()),
        "seed_entries": len(seeds),
        "orphan_seeds": len(by_key - found),
        "sqlite_rows_after_import": database_stats,
        "note": "Unverified drafts are answer-key walkthroughs, not independent confirmations."
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
