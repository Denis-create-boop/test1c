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

@app.route('/show_all_questions', methods=['GET', 'POST'])
def show_all_questions():
    exam, db = exam_database()
    if db is None:
        return redirect(url_for('login'))

    # The database can have gaps in question IDs; paginate actual records, not IDs.
    questions = sorted(
        db.get_all_questions().values(),
        key=lambda question: question["id"],
    )
    per_page = 10
    total = len(questions)
    total_pages = max(1, (total + per_page - 1) // per_page)
    requested_page = request.args.get("page", default=1, type=int) or 1
    page = max(1, min(requested_page, total_pages))
    start = (page - 1) * per_page
    current_questions = questions[start:start + per_page]
    visible_pages = range(max(1, page - 2), min(total_pages, page + 2) + 1)

    return render_template('questions.html', context=exam_context(
        exam,
        title="Все вопросы экзамена",
        questions={index: question for index, question in enumerate(current_questions, 1)},
        is_paginated=True,
        total_questions=total,
        first_number=start + 1 if total else 0,
        last_number=start + len(current_questions),
        page=page,
        total_pages=total_pages,
        pages=visible_pages,
    ))

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
        return render_template("questions.html", context=exam_context(exam,
            title="Вопросы раздела", questions=parts[key]().get_all_questions()))
    options = {}
    for index, name in enumerate(names, 1):
        title = part_titles.get(index, {}).get("text", "Раздел " + str(index))
        options[index] = {"text": title, "db": name}
    return render_template("parts.html", context=exam_context(exam,
        title="Разделы экзамена", questions=options, flag=True, show_category=True))
