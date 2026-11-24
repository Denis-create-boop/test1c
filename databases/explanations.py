"""SQLite store for original, source-backed explanations in both exams.

Question keys include the correct answer to avoid showing an obsolete
explanation after an answer is edited. Section-local numeric IDs differ
from exam IDs, so they are deliberately not part of the key.
"""
import hashlib
import json
import sqlite3
from functools import lru_cache
from pathlib import Path


SEEDS = Path(__file__).with_name("explanation_seeds.json")
DB_FILE = Path(__file__).resolve().parent.parent / "explanations.db"


def _normalize(text):
    return " ".join(str(text or "").split()).casefold()


def question_key(question, answer, answer_text):
    raw = "\n".join((_normalize(question), _normalize(answer), _normalize(answer_text)))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@lru_cache(maxsize=1)
def _seed_items():
    with SEEDS.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _connect():
    connection = sqlite3.connect(str(DB_FILE), timeout=15)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS explanations (
            exam TEXT NOT NULL,
            question_key TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            source_title TEXT NOT NULL,
            source_url TEXT NOT NULL,
            source_type TEXT NOT NULL,
            PRIMARY KEY (exam, question_key)
        )
    """)
    # Seeds are versioned with Git and only fill missing records.
    # A locally edited explanation is never overwritten by a new pull.
    connection.executemany(
        """INSERT OR IGNORE INTO explanations
           (exam, question_key, question, answer, explanation, source_title,
            source_url, source_type)
           VALUES (:exam, :question_key, :question, :answer, :explanation,
                   :source_title, :source_url, :source_type)""",
        [
            {
                **entry,
                "question_key": question_key(entry["question"], entry["answer"], entry["answer_text"]),
            }
            for entry in _seed_items()
        ],
    )
    connection.commit()
    return connection


def find_explanation(exam, question):
    if exam not in ("prof", "erp") or not isinstance(question, dict):
        return None
    answer = str(question.get("answer") or "").strip().lower()
    if answer not in ("a", "b", "c", "d", "e", "f"):
        return None
    key = question_key(question.get("question"), answer, question.get(answer))
    with _connect() as connection:
        row = connection.execute(
            """SELECT explanation, source_title, source_url, source_type
               FROM explanations WHERE exam=? AND question_key=?""",
            (exam, key),
        ).fetchone()
    if row is None:
        return None
    return {
        "text": row[0],
        "source_title": row[1],
        "source_url": row[2],
        "source_type": row[3],
    }
