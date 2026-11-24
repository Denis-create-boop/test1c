"""Explanations for platform and ERP exam questions.

There are two deliberately separate tiers:
1) Curated original explanations with a cited source, stored in
   explanation_seeds.json. A source is not a guarantee that a particular
   historic exam answer remains correct.
2) Automatically produced *unverified answer-key walkthroughs* for every
   other existing question. A walkthrough is NOT an ITS explanation and
   must not be presented as independently checked reasoning.

Both tiers live in SQLite, keyed by exam, question and keyed answer.
Existing curated or manually edited records are never replaced by
generated walkthroughs. Curated seeds can replace generated walkthroughs.
"""
import hashlib
import json
import re
import sqlite3
import threading
from contextlib import closing
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SEEDS = Path(__file__).with_name("explanation_seeds.json")
DB_FILE = ROOT / "explanations.db"
LETTERS = "abcdef"
PARTS = (
    "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
)
EXAMS = {
    "prof": ("all_questions_prof.db", "questions_prof"),
    "erp": ("all_questions_Erp.db", "questions_Erp"),
}
DRAFT_TYPE = "Предварительный разбор по ключу — без проверки по ИТС"
_INIT_LOCK = threading.Lock()
_INITIALIZED = False


def _normalize(value):
    return " ".join(str(value or "").split()).casefold()


def question_key(question, answer, answer_text):
    raw = "\n".join((_normalize(question), _normalize(answer), _normalize(answer_text)))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@lru_cache(maxsize=1)
def _seed_items():
    with SEEDS.open("r", encoding="utf-8") as stream:
        return json.load(stream)


# These are study prompts, not claims that an answer was checked in official ITS.
TOPIC_NOTES = (
    (r"сер(ии|ия|ий|ийн|ийном)|срок[аиу]? годности", "При анализе серий различайте собственно серийный номер, партию, срок годности и политику учёта серий."),
    (r"склад|яче[йек]|размещен|отбор[ау]? товаров|хранени", "В складских вопросах проверьте, что именно настраивается: склад, помещение, область хранения, ячейка или способ обеспечения."),
    (r"начальн\w* остат|ввод\w* остат|ввод\w* задолжен", "При вводе начальных остатков важны вид обязательства, объект расчётов и то, в каком контуре учёта вводятся суммы."),
    (r"взаиморасчет|взаиморасчёт|задолженн|аванс", "Здесь важно отличать задолженность и аванс, а также контрагента, партнёра и объект расчётов."),
    (r"управленческ|бухгалтерск|налогов\w* учет|финансов\w* учет|оперативн\w* учет", "Сопоставляйте контуры учёта: оперативный, управленческий, бухгалтерский, налоговый и международный финансовый."),
    (r"справочник|предопределенн", "Различайте объект метаданных, его экземпляр в информационной базе, группу, владельца и отдельные реквизиты."),
    (r"табличн\w* част", "Табличная часть хранит строки внутри основного объекта; отдельные элементы справочника имеют собственные ссылки."),
    (r"документ|проведен|регистратор", "Проверьте различие между документом, его формой, проведением и движениями, записываемыми в регистры."),
    (r"регистр\w* свед|регистр\w* накопл|регистр\w* бухгалтер|регистр\w* расчет", "Для регистров принципиальны назначение, измерения, ресурсы, периодичность и способ записи."),
    (r"конфигурац|метадан|модул|платформ", "Отделяйте средства платформы от прикладных объектов конфигурации и сохранённых данных информационной базы."),
    (r"клиент|сервер|веб-клиент", "Уточните, где выполняется действие: на клиенте, на сервере или в среде разработки."),
    (r"полн(о)?текстов|поиск", "Обратите внимание на синтаксис оператора поиска и то, какой именно режим поиска описан."),
    (r"рол[ьи]|доступ|разрешен|прав[оа]", "Различайте разрешение на программное действие, интерактивную команду и ограничения по ролям."),
    (r"перечислен|характеристик|дополнительн\w* реквизит", "Проверьте, где задаётся тип значения, набор свойств и допустимость изменения пользователем."),
    (r"планирован|бюджетир|спецификац", "Разделите нормативные параметры, планы, заказы, фактические движения и настройки расчёта."),
    (r"производств|этап|выпуск", "Не смешивайте ресурсную спецификацию, план производства, этап и фактический выпуск продукции."),
    (r"цен[уы]|продаж|соглашени|заказ клиента", "Сопоставляйте условия соглашения, заказ, хозяйственную операцию и фактическое отражение продажи."),
    (r"банк|касс|денежн|платеж|заявк", "Отдельно рассмотрите источник денежных средств, разрешения на платежи и форму распоряжения."),
    (r"организац|подразделен|структур\w* предприятия", "Различайте юридическую организацию, управленческое подразделение и подразделение для кадрового учёта."),
    (r"план счет|субконто|проводк", "Разделите аналитики счёта, отражение хозяйственной операции и правила регламентированного учёта."),
    (r"НДС|налог|счет-фактур", "Обратите внимание на дату налогового события, назначение документа и условия применения налоговых правил."),
)


def _topic_note(question):
    for pattern, note in TOPIC_NOTES:
        if re.search(pattern, question, flags=re.I):
            return note
    return "Сравнивайте объект, операцию, область применения и ограничения, заданные в формулировке вопроса."


def _walkthrough(exam, question):
    """Build a per-question KEY-based comparison without inventing ITS evidence."""
    stem = str(question.get("question") or "").strip()
    answer = str(question.get("answer") or "").lower().strip()
    if answer not in LETTERS:
        return None
    keyed = str(question.get(answer) or "").strip()
    if not stem or not keyed:
        return None

    low = stem.casefold()
    if exam == "prof" and ("нечеткого поиска" in low or "нечёткого поиска" in low):
        return (
            "ВНИМАНИЕ: правильность ключа к этому вопросу вызывает сомнения. "
            "В исходном тесте отмечено: «" + keyed + "». "
            "В современных описаниях полнотекстового поиска операторы могут "
            "отличаться от обозначения в старом вопроснике. "
            "Не заучивайте этот вариант без проверки по руководству именно "
            "вашей версии платформы."
        )
    if exam == "erp" and "расчетов между организациями по реализациям" in low:
        return (
            "ВНИМАНИЕ: в вопросе речь о расчётах между организациями по реализациям, "
            "но существующий ключ указывает: «" + keyed + "». "
            "Это выглядит как смешение задолженности по реализации с авансами "
            "клиентов. Вариант ответа требуется проверить по ERP 2.5; "
            "подтверждённого решения здесь пока нет."
        )

    parts = [
        "В текущем экзаменационном ключе выбран вариант "
        + answer.upper() + ": «" + keyed + "».",
    ]
    direct_options = [
        (i + 1, str(question.get(letter) or "").strip())
        for i, letter in enumerate(LETTERS)
    ]
    lowkey = keyed.casefold()
    combination = bool(re.search(r"вариант|ответ[аыов]? [123456]|все (?:варианты|ответы|указанные)", lowkey))
    if "все варианты" in lowkey or "все указанные ответы" in lowkey:
        available = [(n, t) for n, t in direct_options[:3] if t]
        if available:
            parts.append(
                "Здесь проверяется не один изолированный способ, а набор возможностей. "
                "Первые перечисленные возможности: "
                + "; ".join(str(n) + ") " + text for n, text in available) + "."
            )
            parts.append("Формулировка «все варианты» в исходном ключе объединяет их, а не противопоставляет.")
    elif combination:
        numbers = [
            int(d) for d in re.findall(r"(?<!\d)[1-6](?!\d)", keyed)
        ]
        numbers = list(dict.fromkeys(numbers))
        included = [(n, direct_options[n - 1][1]) for n in numbers if direct_options[n - 1][1]]
        if included:
            parts.append(
                "Выбранный вариант ссылается на следующие пункты: "
                + "; ".join(str(n) + ") " + text for n, text in included) + "."
            )
            if "и/или" in lowkey or " или " in lowkey:
                parts.append(
                    "Союз «или» допускает альтернативные случаи; это не обязательно "
                    "означает одновременное выполнение каждого условия."
                )
            else:
                parts.append(
                    "При таком ответе нужно рассматривать перечисленные пункты вместе "
                    "и проверять, нет ли ограничений в условиях вопроса."
                )
    else:
        alternatives = [
            str(question.get(letter) or "").strip()
            for letter in LETTERS if letter != answer and question.get(letter)
        ]
        if alternatives:
            # Show a concrete alternative, without falsely asserting why it is wrong.
            other = alternatives[0]
            if len(other) > 180:
                other = other[:177].rstrip() + "…"
            parts.append(
                "Для сравнения рассмотрите другой предложенный вариант — «"
                + other + "». Важно определить, почему его область применения "
                "не совпадает с требованием вопроса."
            )

    parts.append(_topic_note(stem))
    parts.append(
        "Это предварительный разбор формулировки и готового ключа, "
        "а не независимо проверенное доказательство правильности. "
        "Ответ нужно сопоставить с актуальной документацией 1С."
    )
    return "\n\n".join(parts)


def _iter_source_questions():
    """Read the same fixed nine-line format as databases.start_questions."""
    header = re.compile(r"^\s*\d+\.\d+\s+(.+?)\s*$")
    for exam in EXAMS:
        for part in PARTS:
            path = ROOT / "questions" / exam / ("part_" + part + ".txt")
            if not path.is_file():
                continue
            lines = path.read_text(encoding="utf-8-sig").splitlines()
            while lines and not lines[-1].strip():
                lines.pop()
            for index in range(0, len(lines), 9):
                block = lines[index:index + 9]
                if len(block) != 9:
                    continue
                match = header.match(block[0])
                if not match:
                    continue
                answer = block[7].strip().lower()
                if answer not in LETTERS:
                    continue
                question = {"question": match.group(1).strip(), "answer": answer}
                for n, letter in enumerate(LETTERS, 1):
                    question[letter] = re.sub(r"^\s*\d+\.\s*", "", block[n]).strip()
                if question.get(answer):
                    yield exam, question


def _iter_live_questions():
    """Also include questions added later via the admin interface."""
    for exam, (name, table) in EXAMS.items():
        db = ROOT / name
        if not db.exists():
            continue
        with closing(sqlite3.connect(str(db), timeout=10)) as connection:
            found = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
            ).fetchone()
            if not found:
                continue
            for row in connection.execute(
                f"SELECT question, answer, a, b, c, d, e, f FROM {table}"
            ):
                question = dict(zip(("question", "answer", *LETTERS), row))
                yield exam, question


def _draft_record(exam, question):
    answer = str(question.get("answer") or "").strip().lower()
    if answer not in LETTERS:
        return None
    correct_text = str(question.get(answer) or "").strip()
    stem = str(question.get("question") or "").strip()
    if not stem or not correct_text:
        return None
    body = _walkthrough(exam, question)
    if not body:
        return None
    return (
        exam,
        question_key(stem, answer, correct_text),
        stem, answer, body,
        "Ключ ответа из существующей базы test1c", "",
        DRAFT_TYPE
    )


def _initialize(connection):
    global _INITIALIZED
    if _INITIALIZED:
        return
    with _INIT_LOCK:
        if _INITIALIZED:
            return
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
        # Upgrade a generated draft when a curated seed becomes available.
        # Never modify curated or user-edited explanations automatically.
        seed_rows = [
            {
                **entry,
                "question_key": question_key(
                    entry["question"], entry["answer"], entry["answer_text"]
                ),
            }
            for entry in _seed_items()
        ]
        connection.executemany(
            """INSERT INTO explanations
               (exam, question_key, question, answer, explanation,
                source_title, source_url, source_type)
               VALUES (:exam, :question_key, :question, :answer, :explanation,
                       :source_title, :source_url, :source_type)
               ON CONFLICT(exam, question_key) DO UPDATE SET
                   question=excluded.question,
                   answer=excluded.answer,
                   explanation=excluded.explanation,
                   source_title=excluded.source_title,
                   source_url=excluded.source_url,
                   source_type=excluded.source_type
               WHERE explanations.source_type=?""".replace(
                   "WHERE explanations.source_type=?",
                   "WHERE explanations.source_type='" + DRAFT_TYPE + "'"
               ),
            seed_rows,
        )
        # The source files ship in Git and are the canonical initial bank.
        # The current SQLite banks may contain additional user questions.
        seen = set()
        drafts = []
        for exam, question in list(_iter_source_questions()) + list(_iter_live_questions()):
            row = _draft_record(exam, question)
            if row and row[:2] not in seen:
                drafts.append(row)
                seen.add(row[:2])
        connection.executemany(
            """INSERT OR IGNORE INTO explanations
               (exam, question_key, question, answer, explanation,
                source_title, source_url, source_type)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            drafts,
        )
        connection.commit()
        _INITIALIZED = True


def _connect():
    connection = sqlite3.connect(str(DB_FILE), timeout=15)
    try:
        _initialize(connection)
    except Exception:
        connection.close()
        raise
    return connection


def find_explanation(exam, question):
    if exam not in EXAMS or not isinstance(question, dict):
        return None
    answer = str(question.get("answer") or "").strip().lower()
    if answer not in LETTERS:
        return None
    key = question_key(question.get("question"), answer, question.get(answer))
    with closing(_connect()) as connection:
        row = connection.execute(
            """SELECT explanation, source_title, source_url, source_type
               FROM explanations WHERE exam=? AND question_key=?""",
            (exam, key),
        ).fetchone()
        if row is None:
            # Covers questions added through the admin interface after startup.
            new = _draft_record(exam, question)
            if new is None:
                return None
            connection.execute(
                """INSERT OR IGNORE INTO explanations
                   (exam, question_key, question, answer, explanation,
                    source_title, source_url, source_type)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                new,
            )
            connection.commit()
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
        "is_draft": row[3] == DRAFT_TYPE,
    }
