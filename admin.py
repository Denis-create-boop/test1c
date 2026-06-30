from flask import Flask, render_template, request
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

    
@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    params = Online().get_params()
    ADMIN = False if int(params["admin"]) == 0 else True
    USER = False if int(params["user"]) == 0 else True
    if ADMIN:
        if request.method == "POST":
            question = request.form["question"]
            option_a = request.form["option_a"]
            option_b = request.form["option_b"]
            option_c = request.form["option_c"]
            option_d = request.form["option_d"]
            option_e = request.form["option_e"]
            QUESTIONSPROF.add_question(question=question, a=option_a, b=option_b, c=option_c, d=option_d, e=option_e)
            context = {
                "titile": "добавление вопроса",
                "message": "вопрос успешно добавлен",
                "info": "добавить еще",
                "url": 'add_question',
                "admin": ADMIN,
                "user": USER,
            }
            
            return render_template('info.html', context=context)
            
        
        else:
            context = {
                "title": "add new question",
                "admin": ADMIN,
                "user": USER,
            }
        
            return render_template('add_question.html', context=context)
    else:
        
        context = {
            "title": "ошибка входа",
            "message": "Вы не авторизованы, пожалуйста войдите в аккаунт",
            "admin": ADMIN,
            "user": USER,
        }
        
        return render_template("info.html", context=context)
    
    
@app.route('/change_question', methods=['GET', 'POST'])
def change_question():
    params = Online().get_params()
    ADMIN = False if int(params["admin"]) == 0 else True
    USER = False if int(params["user"]) == 0 else True
    if ADMIN:
        if request.method == 'POST':
            if "question_id" in request.form.keys():
                quest = QuestionsProf()
                question = quest.get_question(int(request.form["question_id"]))
                context = {
                    "title": "Изменение вопроса",
                    "question": question,
                    "flag": True,
                    "admin": ADMIN,
                    "user": USER,
                }
                
                return render_template("change_question.html", context=context)
            else:
                questions = QuestionsProf()
                new_question = request.form["question"]
                option_a = request.form["option_a"]
                option_b = request.form["option_b"]
                option_c = request.form["option_c"]
                option_d = request.form["option_d"]
                option_e = request.form["option_e"]
                option_f = request.form["option_f"]
                answer = request.form["answer"]
                id = request.form["id"]
                questions.change_question(id=id, question=new_question, answer=answer, a=option_a, b=option_b, c=option_c, d=option_d, e=option_e, f=option_f)
                context = {
                    "title": "изменение вопроса",
                    "message": "вопрос успешно изменен",
                    "info": "изменить еще",
                    "url": 'change_question',
                    "admin": ADMIN,
                    "user": USER,
                }
                
                return render_template("info.html", context=context)
        else:
        
            context = {
                "title": "Изменение вопроса",
                "flag": False,
                "admin": ADMIN,
                "user": USER,
            }
        
            return render_template("change_question.html", context=context)    
 
    else:
        context = {
            "title": "ошибка входа",
            "message": "Вы не авторизованы, пожалуйста войдите в аккаунт",
            "admin": ADMIN,
            "user": USER,
        }
        
        return render_template("info.html", context=context)
    
    
@app.route('/show_all_questions', methods=["GET", "POST"])
def show_all_questions():
    params = Online().get_params()
    ADMIN = False if int(params["admin"]) == 0 else True
    USER = False if int(params["user"]) == 0 else True
    if ADMIN:
        if request.method == 'POST':
            question = QUESTIONSPROF.get_question(id=request.form['id'])
            
            context = {
                "questions": question,
                "title": "Просмотр вопроса",
                "admin": ADMIN,
                "user": USER,
            }
            
            return render_template('questions.html', context=context)
        
        else:
            questions = QUESTIONSPROF.get_all_questions()
            context = {
                "questions": questions,
                "title": "Все вопросы",
                "admin": ADMIN,
                "user": USER,
            }
        return render_template('questions.html', context=context)
    
    else:
        context = {
            "title": "ошибка входа",
            "message": "Вы не авторизованы, пожалуйста войдите в аккаунт",
            "admin": ADMIN,
            "user": USER,
        }
        
        return render_template("info.html", context=context)
    
    
@app.route("/show_question", methods=["GET", "POST"])
def show_question():
    params = Online().get_params()
    ADMIN = False if int(params["admin"]) == 0 else True
    USER = False if int(params["user"]) == 0 else True
    if ADMIN:
        if request.method == "POST":
            question = QuestionsProf().get_question(id=request.form["question_id"])
            
            context = {
                "title": "просмотр вопроса",
                "flag": True,
                "question": question,
                "admin": ADMIN,
                "user": USER,
            }
            return render_template("show_question.html", context=context)
        
        else:
            context = {
                "title": "просмотр вопроса",
                "flag": False,
                "admin": ADMIN,
                "user": USER,
            }
            return render_template("show_question.html", context=context)
    
    else:
        context = {
            "title": "ошибка входа",
            "message": "Вы не авторизованы, пожалуйста войдите в аккаунт",
            "flag": False,
            "admin": ADMIN,
            "user": USER,
        }
        
        return render_template("info.html", context=context)
    
    
    
@app.route("/categories", methods=["GET", "POST"])
def categories():
    params = Online().get_params()
    ADMIN = False if int(params["admin"]) == 0 else True
    USER = False if int(params["user"]) == 0 else True
    
    CATEGORIES = {1: {'text': '1 общие механизмы, понятия и термины', 'db': "PartOne"},
                    2: {'text': '2 Редакторы и инструменты общие', 'db': "PartTwo"},
                    3: {'text': '3 Редакторы и инструменты режима разработки', 'db': "PartThree"},
                    4: {'text': '4 Конструкторы', 'db': "PartFour"},
                    5: {'text': '5 Технология разработки', 'db': "PartFive"},
                    6: {'text': '6 Объектная модель прикладного решения', 'db': "PartSix"},
                    7: {'text': '7 Табличная модель прикладного решения', 'db': "PartSeven"},
                    8: {'text': '8 Механизмы интеграции и обмена данными', 'db': "PartEight"},
                    9: {'text': '9 Система взаимодействия', 'db': "PartNine"},
                    10: {'text': '10 Интерфейсные механизмы', 'db': "PartTen"},
                    11: {'text': '11 Механизмы построения отчетности', 'db': "PartEleven"},
                    12: {'text': '12 Механизмы оперативного учета', 'db': "PartTwelve"},
                    13: {'text': '13 Объекты и механизмы бухгалтирского учета', 'db': "PartThirteen"},
                    14: {'text': '14 Механизмы сложных переодических расчетов', 'db': "PartFourteen"}}
    
    
    if ADMIN:
        if request.method == "POST":
            str_db = request.form["db"]
            class_db = {"PartOne": PartOneProf,
                        "PartTwo": PartTwoProf,
                        "PartThree": PartThreeProf,
                        "PartFour": PartFourProf,
                        "PartFive": PartFiveProf,
                        "PartSix": PartSixProf,
                        "PartSeven": PartSevenProf,
                        "PartEight": PartEightProf,
                        "PartNine": PartNineProf,
                        "PartEleven": PartElevenProf,
                        "PartTwelve": PartTwelveProf,
                        "PartThirteen": PartThirteenProf,
                        "PartFourteen": PartFourteenProf}
            
            db = class_db[str_db]
            
            questions = db().get_all_questions()
            title = None
            
            for k, v in CATEGORIES.items():
                if v["db"] == str_db:
                    title = v["text"][2:]
                    break      
            
            context = {
                "questions": questions,
                "title": f"Все вопросы по категории '{title}'",
                "admin": ADMIN,
                "user": USER,
            }
            return render_template('questions.html', context=context)
            
        
        else:
            context = {
                'questions': CATEGORIES,
                'flag': True,
                "show_category": True,
                "admin": ADMIN,
                "user": USER,
            }

            return render_template('parts.html', context= context)
    
    else:
        context = {
            "title": "ошибка входа",
            "message": "Вы не авторизованы, пожалуйста войдите в аккаунт",
            "flag": False,
            "admin": ADMIN,
            "user": USER,
        }