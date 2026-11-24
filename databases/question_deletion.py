"""Safe deletion of an exam question from both the catalogue and its section."""
import os
import sqlite3


EXAM_STORAGE = {
    "prof": ("all_questions_prof.db", "questions_prof", "questions_prof.db"),
    "erp": ("all_questions_Erp.db", "questions_Erp", "questions_Erp.db"),
}
MATCH_COLUMNS = ("question", "answer", "a", "b", "c", "d", "e", "f", "image")


def delete_exam_question(exam, question_id):
    """Delete one catalogue entry and its exact section counterpart in one transaction.

    Returns False if the specified catalogue ID does not exist. If matching against
    sections is ambiguous, abort without changing either SQLite database.
    """
    if exam not in EXAM_STORAGE:
        raise ValueError("Неизвестный экзамен.")
    main_path, main_table, section_path = EXAM_STORAGE[exam]
    if not os.path.isfile(main_path):
        return False

    with sqlite3.connect(main_path, timeout=15) as connection:
        if os.path.isfile(section_path):
            connection.execute("ATTACH DATABASE ? AS sections", (section_path,))
            has_sections = True
        else:
            has_sections = False

        connection.execute("BEGIN IMMEDIATE")
        columns = ", ".join(MATCH_COLUMNS)
        source = connection.execute(
            f"SELECT rowid, {columns} FROM main.{main_table} WHERE id=? LIMIT 1",
            (question_id,),
        ).fetchone()
        if source is None:
            return False

        source_rowid = source[0]
        source_fields = source[1:]
        if has_sections:
            table_names = [
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sections.sqlite_master WHERE type='table'"
                ).fetchall()
                if row[0].lower().startswith("part_")
            ]
            matches = []
            predicates = " AND ".join(f"{column} IS ?" for column in MATCH_COLUMNS)
            for table in table_names:
                # Table names originate in sqlite_master, not an HTTP parameter.
                quoted_table = '"' + table.replace('"', '""') + '"'
                for match in connection.execute(
                    f"SELECT rowid FROM sections.{quoted_table} "
                    f"WHERE {predicates}",
                    source_fields,
                ).fetchall():
                    matches.append((quoted_table, match[0]))

            if len(matches) > 1:
                raise ValueError(
                    "В разделах найдено несколько одинаковых вопросов. "
                    "Удаление остановлено, чтобы не затронуть лишние записи."
                )
            if matches:
                matched_table, matched_rowid = matches[0]
                connection.execute(
                    f"DELETE FROM sections.{matched_table} WHERE rowid=?",
                    (matched_rowid,),
                )

        connection.execute(
            f"DELETE FROM main.{main_table} WHERE rowid=?",
            (source_rowid,),
        )
    return True
