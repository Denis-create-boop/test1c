from flask import Flask, render_template, request, redirect, url_for, abort
from databases.questions_prof import *
from databases.questions_erp import *
from databases.users import Users
from databases.params import *
import os
import sys
import time


if getattr(sys, 'frozen', False):
    base_path = sys.executable
else:
    base_path = __file__

base_dir = os.path.dirname(base_path)
static_folder = os.path.join(base_dir, 'static')
template_folder = os.path.join(base_dir, 'templates')

app = Flask(__name__) #, static_folder=static_folder, template_folder=template_folder)


QUESTIONSPROF = QuestionsProf()
QUESTIONSERP = QuestionsErp()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)         
 

@app.route('/login', methods=['GET', 'POST'])
def login():
    admin = False
    user = False
    params = Online()
    if request.method == 'POST':
        user_login = Users()
        try:
            data = user_login.get_login_and_password(request.form["login"])
        except:
            data = {}
        if data: 
            if request.form["login"] == data["login"] and request.form["password"] == data["password"]:
                if data["admin"] == '1':
                    admin = True
                    user = False 
                    context = {
                        "title": "administrator",
                        "message": "",
                        "admin": admin,
                        "user": user,
                    }
                else:
                    user = True
                    admin = False
                    context = {
                        "title": "1c",
                        "message": "",
                        "admin": admin,
                        "user": user,
                    }

                params.change_params(admin, user)
                return render_template("index.html", context=context)
            else:
                context = {
                    "title": "login",
                    "message": "Неверный логин или пароль",
                }

                return render_template('login.html', context=context)
        else:
            context = {
                "title": "login",
                "message": "Неверный логин или пароль",
            }
            
            return render_template('login.html', context=context)
    else:
        params = Online().get_params()
        admin = False if int(params["admin"]) == 0 else True
        user = False if int(params["user"]) == 0 else True
        
        if admin:
            title = "administrator"

        elif user:
            title = "1c"

        else:
            title = "login"
            
        context = {
            "title": title,
            "message": "",
            "admin": admin,
            "user": user,
        }
        
        return render_template("login.html", context=context)

    

EXAM_LABELS = {"prof": "1С:Профессионал по платформе", "erp": "1С:ERP Управление предприятием"}

def exam_database():
    p = Online().get_params()
    if not bool(int(p["admin"])):
        abort(403)
    exam = request.values.get("exam")
    if exam not in EXAM_LABELS:
        return None, None
    return exam, QuestionsProf() if exam == "prof" else QuestionsErp()

def exam_context(exam, **kwargs):
    context = {"admin": True, "exam": exam, "exam_title": EXAM_LABELS[exam]}
    context.update(kwargs)
    return context

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    exam, db = exam_database()
    if db is None:
        return redirect(url_for('login'))
    if request.method == "POST":
        values = {k: request.form.get(k, "").strip() for k in
                  ("question", "option_a", "option_b", "option_c", "option_d", "option_e", "answer")}
        answer = values["answer"].lower()
        if (not values["question"] or any(not values["option_" + k] for k in ("a", "b", "c"))
                or answer not in ("a", "b", "c", "d", "e")
                or not values.get("option_" + answer, "")):
            return render_template('add_question.html',
                context=exam_context(exam, values=values,
                    message="Заполните вопрос и выберите правильный вариант с текстом.")), 400
        db.add_question(question=values["question"], answer=answer,
            a=values["option_a"], b=values["option_b"], c=values["option_c"],
            d=values["option_d"] or None, e=values["option_e"] or None)
        return render_template('info.html', context=exam_context(exam,
            title="Добавление вопроса", message="Вопрос успешно добавлен",
            info="Добавить ещё", url="add_question"))
    return render_template('add_question.html', context=exam_context(exam, title="Добавление вопроса"))

@app.route('/change_question', methods=['GET', 'POST'])
def change_question():
    exam, db = exam_database()
    if db is None:
        return redirect(url_for('login'))
    if request.method == "POST":
        if "question_id" in request.form:
            try:
                q = db.get_question(int(request.form["question_id"]))
            except ValueError:
                abort(400)
            if not q:
                return render_template('change_question.html', context=exam_context(exam,
                    flag=False, message="Вопрос не найден.")), 404
            return render_template('change_question.html',
                context=exam_context(exam, flag=True, question=q))
        try:
            question_id = int(request.form["id"])
        except (ValueError, KeyError):
            abort(400)
        old = db.get_question(question_id)
        if not old:
            abort(404)
        values = {k: request.form.get("option_" + k, "").strip()
                  for k in ("a", "b", "c", "d", "e", "f")}
        answer = request.form.get("answer", "").lower()
        question = request.form.get("question", "").strip()
        if not question or any(not values[k] for k in ("a", "b", "c")) or answer not in values or not values[answer]:
            return render_template('change_question.html', context=exam_context(exam,
                flag=True, question=dict(old, question=question, answer=answer, **values),
                message="Заполните вопрос, варианты и правильный ответ.")), 400
        db.change_question(id=question_id, question=question, answer=answer,
            a=values["a"], b=values["b"], c=values["c"],
            d=values["d"] or None, e=values["e"] or None, f=values["f"] or None,
            image=old.get("image"))
        return render_template('info.html', context=exam_context(exam,
            title="Изменение вопроса", message="Вопрос изменён", info="Изменить ещё", url="change_question"))
    return render_template('change_question.html', context=exam_context(exam, flag=False))

def render_admin_question_list(exam, questions, category_key=None, category_title=None):
    """Render one page from the specified exam or section."""
    ordered = sorted(questions.values(), key=lambda question: question["id"])
    per_page = 10
    total = len(ordered)
    total_pages = max(1, (total + per_page - 1) // per_page)
    requested_page = request.args.get("page", default=1, type=int) or 1
    page = max(1, min(requested_page, total_pages))
    start = (page - 1) * per_page

    return render_template("questions.html", context=exam_context(
        exam,
        title="Вопросы раздела" if category_key else "Все вопросы экзамена",
        questions=ordered[start:start + per_page],
        is_paginated=True,
        category_key=category_key,
        category_title=category_title,
        total_questions=total,
        first_number=start + 1 if total else 0,
        last_number=min(start + per_page, total),
        page=page,
        total_pages=total_pages,
        pages=range(max(1, page - 2), min(total_pages, page + 2) + 1),
    ))


@app.route('/show_all_questions', methods=['GET'])
def show_all_questions():
    exam, db = exam_database()
    if db is None:
        return redirect(url_for('login'))
    return render_admin_question_list(exam, db.get_all_questions())


@app.route('/show_question', methods=['GET', 'POST'])
def show_question():
    exam, db = exam_database()
    if db is None:
        return redirect(url_for('login'))
    if request.method == "POST":
        try:
            q = db.get_question(int(request.form["question_id"]))
        except (ValueError, KeyError):
            abort(400)
        if not q:
            return render_template('show_question.html',
                context=exam_context(exam, flag=False, message="Вопрос не найден.")), 404
        return render_template('show_question.html',
            context=exam_context(exam, flag=True, question=q))
    return render_template('show_question.html', context=exam_context(exam, flag=False))

@app.route("/categories", methods=["GET", "POST"])
def categories():
    exam, db = exam_database()
    if db is None:
        return redirect(url_for("login"))
    names = ("One", "Two", "Three", "Four", "Five", "Six", "Seven",
             "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen")
    parts = {name: globals()["Part" + name + ("Prof" if exam == "prof" else "Erp")]
             for name in names}
    part_titles = PartsProf().get_parts() if exam == "prof" else PartsErp().get_parts()

    if request.method == "POST":
        key = request.form.get("db")
        if key not in parts:
            abort(400)
        return redirect(url_for("categories", exam=exam, db=key))

    key = request.args.get("db")
    if key is not None:
        if key not in parts:
            abort(404)
        category_number = names.index(key) + 1
        category_title = part_titles.get(category_number, {}).get(
            "text", "Раздел " + str(category_number))
        return render_admin_question_list(
            exam, parts[key]().get_all_questions(),
            category_key=key, category_title=category_title,
        )

    options = {}
    for index, name in enumerate(names, 1):
        title = part_titles.get(index, {}).get("text", "Раздел " + str(index))
        options[index] = {"text": title, "db": name}
    return render_template("parts.html", context=exam_context(
        exam, title="Разделы экзамена", questions=options,
        flag=True, show_category=True,
    ))


@app.route("/delete_question", methods=["GET", "POST"])
def delete_question():
    exam, db = exam_database()
    if db is None:
        return redirect(url_for("login"))

    from databases.question_deletion import delete_exam_question

    try:
        question_id = int(request.values.get("id", ""))
        if question_id < 1:
            raise ValueError()
    except (TypeError, ValueError):
        abort(400)

    question = db.get_question(question_id)
    if not question:
        return render_template("delete_question.html", context=exam_context(
            exam, question=None, message="Вопрос не найден.")), 404

    return_page = request.values.get("page", default="1")
    if not return_page.isdigit() or int(return_page) < 1:
        return_page = "1"
    if request.method == "POST":
        if request.form.get("confirmation") != "delete":
            return render_template("delete_question.html", context=exam_context(
                exam, question=question, page=return_page,
                message="Для удаления необходимо установить отметку подтверждения.",
            )), 400
        try:
            deleted = delete_exam_question(exam, question_id)
        except ValueError as error:
            return render_template("delete_question.html", context=exam_context(
                exam, question=question, page=return_page, message=str(error),
            )), 409
        if not deleted:
            abort(404)
        return redirect(url_for("show_all_questions", exam=exam,
                                page=return_page, deleted=question_id))

    return render_template("delete_question.html", context=exam_context(
        exam, question=question, page=return_page,
    ))
