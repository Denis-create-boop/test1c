from admin import *
from databases.start_questions import *
import random


QUESTIONS = []
ANSWERS_LIST = []
COUNT = 1
FLAG = False
EXAM_COUNT = 0
PROF = False
ERP = False

part_list_prof = [PartOneProf(), PartTwoProf(), PartThreeProf(), PartFourProf(), PartFiveProf(), PartSixProf(), PartSevenProf(), PartEightProf(), 
                  PartNineProf(), PartTenProf(), PartElevenProf(), PartTwelveProf(), PartThirteenProf(), PartFourteenProf()]

part_list_erp = [PartOneErp(), PartTwoErp(), PartThreeErp(), PartFourErp(), PartFiveErp(), PartSixErp(), PartSevenErp(), PartEightErp(), PartNineErp(), 
                 PartTenErp(), PartElevenErp(), PartTwelveErp(), PartThirteenErp(), PartFourteenErp()]

question_misstakes = 0
answers = 0

params = Online().get_params()
ADMIN = False if int(params["admin"]) == 0 else  True
USER = False if int(params["user"]) == 0 else True


def study_for_parts(title, url, questions, back_flag=False, flag=False):
    global COUNT, FLAG
    FLAG = True
    
    first = False
    if flag:
        all_questions = questions
        last_id = len(questions)
    else:
        all_questions = questions.get_all_questions()
        last_id = questions.get_last_id()
        
    if back_flag:
        if COUNT == last_id or COUNT == last_id + 1:
            COUNT -= 2

        else:
            if COUNT == 1:
                COUNT = last_id - 1
            else:    
                COUNT -= 2
            
    if COUNT == last_id:
        if flag:
            question = all_questions[COUNT - 1]
        else:
            question = all_questions[COUNT]
        context = {
            "title": title,
            "question": question,
            "url": url,
            "flag": True,
            "first_question": first,
            "last_question": True
        }

        COUNT = 1
    else:
        if COUNT == 1:
            first = True
        
        if flag:
            question = all_questions[COUNT-1]
            
        else:
            question = all_questions[COUNT]

        context = {
            "title": title,
            "question": question,
            'url': url,
            'flag': True,
            "first_question": first,
            'last_question': False,
        }
        COUNT += 1
    return context


def writing_questions(exam):
    global QUESTIONS, ERP, PROF, part_list_prof, part_list_erp
    if exam == "prof":
        questions = QuestionsProf()
        part_list = part_list_prof
        PROF = True
        ERP = False
        
    elif exam == "erp":
        questions = QuestionsErp()
        part_list = part_list_erp
        ERP = True
        PROF = False
        
    last_id = questions.get_last_id()
    
    for part in part_list:
        last_id = part.get_last_id()
        number = random.randrange(1, last_id)
        question = part.get_question(number)
        QUESTIONS.append(question)
        random.shuffle(QUESTIONS) 
            
 
def write():
   
    data_prof = {1: {"path": "./questions/prof/part_one.txt", "db": PartOneProf()},
                2: {"path": "./questions/prof/part_two.txt", "db": PartTwoProf()},
                3: {"path": "./questions/prof/part_three.txt", "db": PartThreeProf()},
                4: {"path": "./questions/prof/part_four.txt", "db": PartFourProf()},
                5: {"path": "./questions/prof/part_five.txt", "db": PartFiveProf()},
                6: {"path": "./questions/prof/part_six.txt", "db": PartSixProf()},
                7: {"path": "./questions/prof/part_seven.txt", "db": PartSevenProf()},
                8: {"path": "./questions/prof/part_eight.txt", "db": PartEightProf()},
                9: {"path": "./questions/prof/part_nine.txt", "db": PartNineProf()},
                10: {"path": "./questions/prof/part_ten.txt", "db": PartTenProf()},
                11: {"path": "./questions/prof/part_eleven.txt", "db": PartElevenProf()},
                12: {"path": "./questions/prof/part_twelve.txt", "db": PartTwelveProf()},
                13: {"path": "./questions/prof/part_thirteen.txt", "db": PartThirteenProf()},
                14: {"path": "./questions/prof/part_fourteen.txt", "db": PartFourteenProf()}}
        
    parts_prof = {
            1: {"text": '1 общие механизмы, понятия и термины', "url": 'part_one'},
            2: {"text": '2 Редакторы и инструменты общие', "url": 'part_two'},
            3: {"text": '3 Редакторы и инструменты режима разработки', "url": 'part_three'},
            4: {"text": '4 Конструкторы', "url": 'part_four'},
            5: {"text": '5 Технология разработки', "url": 'part_five'},
            6: {"text": '6 Объектная модель прикладного решения', "url": 'part_six'},
            7: {"text": '7 Табличная модель прикладного решения', "url": 'part_seven'},
            8: {"text": '8 Механизмы интеграции и обмена данными', "url": 'part_eight'},
            9: {"text": '9 Система взаимодействия', "url": 'part_nine'},
            10: {"text": '10 Интерфейсные механизмы', "url": 'part_ten'},
            11: {"text": '11 Механизмы построения отчетности', "url": 'part_eleven'},
            12: {"text": '12 Механизмы оперативного учета', "url": 'part_twelve'},
            13: {"text": '13 Объекты и механизмы бухгалтирского учета', "url": 'part_thirteen'},
            14: {"text": '14 Механизмы сложных переодических расчетов', "url": 'part_fourteen'}
        }
        
        
    
    data_erp = {1: {"path": "./questions/erp/part_one.txt", "db": PartOneErp()},
                2: {"path": "./questions/erp/part_two.txt", "db": PartTwoErp()},
                3: {"path": "./questions/erp/part_three.txt", "db": PartThreeErp()},
                4: {"path": "./questions/erp/part_four.txt", "db": PartFourErp()},
                5: {"path": "./questions/erp/part_five.txt", "db": PartFiveErp()},
                6: {"path": "./questions/erp/part_six.txt", "db": PartSixErp()},
                7: {"path": "./questions/erp/part_seven.txt", "db": PartSevenErp()},
                8: {"path": "./questions/erp/part_eight.txt", "db": PartEightErp()},
                9: {"path": "./questions/erp/part_nine.txt", "db": PartNineErp()},
                10: {"path": "./questions/erp/part_ten.txt", "db": PartTenErp()},
                11: {"path": "./questions/erp/part_eleven.txt", "db": PartElevenErp()},
                12: {"path": "./questions/erp/part_twelve.txt", "db": PartTwelveErp()},
                13: {"path": "./questions/erp/part_thirteen.txt", "db": PartThirteenErp()},
                14: {"path": "./questions/erp/part_fourteen.txt", "db": PartFourteenErp()}}
        
    parts_erp = {
            1: {"text": '1 Общие положения, нормативно-справочная информация', "url": 'part_one'},
            2: {"text": '2 Планирование', "url": 'part_two'},
            3: {"text": '3 Бюджетирование', "url": 'part_three'},
            4: {"text": '4 Работа с заказами', "url": 'part_four'},
            5: {"text": '5 Закупки', "url": 'part_five'},
            6: {"text": '6 Складское хозяйство', "url": 'part_six'},
            7: {"text": '7 Продажи', "url": 'part_seven'},
            8: {"text": '8 Казначейство', "url": 'part_eight'},
            9: {"text": '9 Ведение взаиморасчетов', "url": 'part_nine'},
            10: {"text": '10 Нормирование', "url": 'part_ten'},
            11: {"text": '11 Управление производством', "url": 'part_eleven'},
            12: {"text": '12 Производство', "url": 'part_twelve'},
            13: {"text": '13 Оперативный учет', "url": 'part_thirteen'},
            14: {"text": '14 Регламентированный учет', "url": 'part_fourteen'}
        }
        
    if QuestionsProf().get_last_id() == 0:    
        for k, v in data_prof.items():
            write_to_db_questions(v["path"], v["db"], 'prof')
    
    if QuestionsErp().get_last_id() == 0:
        for k, v in data_erp.items():
            write_to_db_questions(v["path"], v["db"], 'erp')
            
            
    if PartsProf().get_last_id() == 0:    
        write_to_db_parts(parts_prof, PartsProf())
        
    if PartsErp().get_last_id() == 0:
        write_to_db_parts(parts_erp, PartsErp())
 
 
def get_context(title, questions, url, flag, first_question, last_question):
    global ADMIN, USER, COUNT

    all_questions = questions.get_all_questions()
    
    context = {
        "title": title,
        "question": all_questions[COUNT],
        "url": url,
        "flag": flag,
        "first_question": first_question,
        "last_question": last_question,
        "admin": ADMIN,
        "user": USER,
    }    
    
    return context                        
 
    
@app.route('/', methods=['GET', 'POST'])
def index():
    global COUNT, QUESTIONS, EXAM_COUNT, ANSWERS_LIST, ADMIN, USER, params, question_misstakes
    
    ADMIN = False if int(params["admin"]) == 0 else  True
    USER = False if int(params["user"]) == 0 else True
    
    create_account(flag=True)
    create_account()
    
    QUESTIONS = []
    EXAM_COUNT = 0
    ANSWERS_LIST = []
    COUNT = 1
    question_misstakes = 0
    
    if request.method == 'POST':
        
        context = {
            'title': '1c', 
            'flag': True,
            "user": USER,
            "admin": ADMIN,

        }
        if ADMIN or USER:
            return render_template('index.html', context=context)
        else:
            return render_template('login.html', context=context)
    else:
        context = {
            'title': '1c', 
            'flag': False,
            "admin": ADMIN,
            "user": USER,
            "platformaprof": False,
            "ERP": False,

        }
        if ADMIN or USER:
            
            return render_template('index.html', context=context)
        else:
            return render_template('login.html', context=context)

@app.route('/test_erp')
def test_erp():

    writing_questions("erp")
    
    context = {
        "title": "Экзамен",
        'url': 'test_quest',
        "admin": ADMIN,
        "user": USER,
        "ERP": True,
        "platformaprof": False,
    }
    
    return render_template('index.html', context=context)    


@app.route("/test_prof")
def test_prof():
    writing_questions("prof")
    
    context = {
        "title": "Экзамен",
        'url': 'test_quest',
        "admin": ADMIN,
        "user": USER,
        "ERP": False,
        "platformaprof": True,
    }
    return render_template('index.html', context=context)  


@app.route('/test')
def test():
    global FLAG, COUNT, ADMIN, USER, question_misstakes
    COUNT = 1
    FLAG = False
    question_misstakes = 0

        
    context = {
            "title": "Экзамен",
            'url': 'test_quest',
            "admin": ADMIN,
            "user": USER,
        }

    return render_template('test.html', context=context)
    
@app.route('/test_with_answers') 
def test_with_answers():
    global QUESTIONS, FLAG, COUNT, ADMIN, USER, PROF, ERP, part_list_prof, part_list_erp, question_misstakes
    COUNT = 1
    FLAG = True
    QUESTIONS = []
    question_misstakes = 0

    if PROF:
        questions = QuestionsProf()
        part_list = part_list_prof
    elif ERP:
        questions = QuestionsErp()
        part_list = part_list_erp
        
    last_id = questions.get_last_id()
    
    for part in part_list:
        last_id = part.get_last_id()
        number = random.randrange(1, last_id)
        question = part.get_question(number)
        QUESTIONS.append(question)

    context = {
        "title": "Экзамен с ответами",
        'url': 'test_quest',
        "admin": ADMIN,
        "user": USER,
    }
    
    return render_template('test.html', context=context)
 
    
@app.route('/test_quest', methods=['GET', "POST"])
def test_quest():
    global QUESTIONS, FLAG, COUNT, ADMIN, USER, ANSWERS_LIST, question_misstakes, answers

    title = "Экзамен"
    url = "test_quest"
    context = None
    
    def misstakes():
        global question_misstakes, answers
        ANSWERS_LIST.append(request.form['answer'])
        if request.form["answer"] != QUESTIONS[COUNT -3]["answer"]:
            question_misstakes += 1
        else:
            answers += 1

        misstake_dict = {
            0: "ошибок",
            1: "ошибку",
            2: "ошибки",
            3: "ошибки",
            4: "ошибки",
            5: "ошибок",
            6: "ошибок",
            7: "ошибок",
            8: "ошибок",
            9: "ошибок",
            10: "ошибок",
            11: "ошибок",
            12: "ошибок",
            13: "ошибок",
            14: "ошибок"
        }
        
        if question_misstakes > 2:
            result = f"Тест не сдан вы совершили {question_misstakes} {misstake_dict[question_misstakes]}"
        else:
            result = f"Поздровляем тест сдан вы совершили {question_misstakes} {misstake_dict[question_misstakes]}"

        context = {
            "title": "Результат",
            "result": result,
            "misstakes": question_misstakes,
            "flag": FLAG,
            "admin": ADMIN,
            "user": USER,
        }
        
        return render_template('result.html', context=context)
    
    
    if COUNT <= 15:
        if COUNT == 15:
            if request.method == "POST":
                try:
                    if request.form["toBack"] == "True":
                        context = study_for_parts(title, url, QUESTIONS, back_flag=True, flag=True)
                        ANSWERS_LIST.pop()  
                        return render_template('test.html', context=context) 
                    else:
                        COUNT += 1
                        return(misstakes())
                except:
                    COUNT +=1
                    return(misstakes())
                  
        else:
            if request.method == 'POST':
                try:
                    if request.form["toBack"] == 'True':
                        if COUNT == 2:
                            context = study_for_parts(title, url, QUESTIONS, back_flag=True, flag=True)
                            ANSWERS_LIST.pop()
                        else:
                            context = study_for_parts(title, url, QUESTIONS, back_flag=True, flag=True)
                            ANSWERS_LIST.pop()
                            
                    else:
                        ANSWERS_LIST.append(request.form['answer'])
                        if request.form["answer"] != QUESTIONS[COUNT -2]["answer"]:
                            question_misstakes += 1
                        else:
                            answers += 1
                        
                        question = QUESTIONS[COUNT - 1]
                        question["id"] = COUNT
                        context = {
                            "question": question,
                            "flag": FLAG,
                            'url': url,
                            "title": title,
                            "first_question": False,
                            "last_question": False,
                            "misstakes": question_misstakes,
                            "admin": ADMIN,
                            "user": USER,
                        }
                        COUNT += 1
                except:
                        ANSWERS_LIST.append(request.form['answer'])
                        print(request.form["answer"])
                        print(QUESTIONS[COUNT - 2]["answer"])
                        print(request.form["answer"] == QUESTIONS[COUNT - 2]["answer"])
                        if request.form["answer"] != QUESTIONS[COUNT -2]["answer"]:
                            question_misstakes += 1
                        else:
                            answers += 1
                        question = QUESTIONS[COUNT - 1]
                        question["id"] = COUNT
                        context = {
                            "question": question,
                            "flag": FLAG,
                            'url': url,
                            "title": title,
                            "first_question": False,
                            "last_question": False,
                            "misstakes": question_misstakes,
                            "admin": ADMIN,
                            "user": USER,
                        }
                        COUNT += 1

            else:
                question = QUESTIONS[COUNT - 1]
                question["id"] = COUNT
                COUNT += 1

                context = {
                    "question": question,
                    "flag": FLAG,
                    'url': url,
                    "title": title,
                    "first_question": True,
                    "last_question": False,
                    "misstakes": question_misstakes,
                    "admin": ADMIN,
                    "user": USER,
                }

            return render_template('test.html', context=context)
    else:
        misstakes()

        
@app.route('/show_misstakes')
def show_misstakes():
    global  ANSWERS_LIST, EXAM_COUNT, ADMIN, USER
    
    variants = ["a", "b", "c", "d", "e", "f"]
    
    if EXAM_COUNT < 14:
        url = 'show_misstakes'
        message = "Следующий вопрос"
        question = QUESTIONS[EXAM_COUNT]
        answer = ANSWERS_LIST[EXAM_COUNT]
        EXAM_COUNT += 1
    else:
        url = 'index'
        message = "На главную"
  
    if EXAM_COUNT < 14:
        context = {
            "title": "Посмотреть ошибки",
            "question": question,
            "answer": answer,
            "url": url,
            "message": message,
            "variants": variants,
            "flag": True,
            "admin": ADMIN,
            "user": USER,
        }
    elif EXAM_COUNT == 14:
        context = {
            "title": "Посмотреть ошибки",
            "question": question,
            "answer": answer,
            "url": url,
            "variants": variants,
            "message": message,
            "flag": False,
            "admin": ADMIN,
            "user": USER,
        }
    else:
        context = {
            "title": "Посмотреть ошибки",
            "flag": False,
            "admin": ADMIN,
            "user": USER,
        }

    return render_template('answers.html', context=context)


@app.route('/study')
def study():
    global COUNT, ADMIN, USER, ERP, PROF
    COUNT = 1

    if PROF:
        parts = PartsProf().get_parts()
    elif ERP:
        parts = PartsErp().get_parts()
        
    context = {
            'questions': parts,
        'flag': True,
        "show_category": False,
        "admin": ADMIN,
        "user": USER,
    }
    
    
    return render_template('parts.html', context= context)
 
 
@app.route('/part_one', methods=['GET', 'POST'])
def part_one():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    
    url = "part_one"
    
    if PROF:
        questions = PartOneProf()
        title = "общие механизмы, понятия и термины"
    elif ERP:
        questions = PartOneErp()
        title = "Общие положения, нормативно-справочная информация"
    
    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)
 
 
@app.route('/part_two', methods=['GET', 'POST'])
def part_two():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    url = "part_two"
    
    if PROF:
        questions = PartTwoProf() 
        title = "Редакторы и инструменты общие"
    elif ERP:
        questions = PartTwoErp()
        title = "Планирование"
    
    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)    
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_three', methods=['GET', 'POST'])
def part_three():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    url = "part_three"

    if PROF:
        questions = PartThreeProf()
        title = "Редакторы и инструменты режима разработки"
    elif ERP:
        questions = PartThreeErp()
        title = "Бюджетирование"
    
    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)
 
 
@app.route('/part_four', methods=['GET', 'POST'])
def part_four():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    url = "part_four"
    if PROF:
        questions = PartFourProf()
        title = "Конструкторы"
    elif ERP:
        questions = PartFourErp()
        title = "Работа с заказами"
        
    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_five', methods=['GET', 'POST'])
def part_five():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    
    url = "part_five"

    if PROF:
        questions = PartFiveProf()
        title = "Технология разработки"
    elif ERP:
        questions = PartFiveErp()
        title = "Закупки"
    
    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_six', methods=['GET', 'POST'])
def part_six():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    
    url = "part_six"

    if PROF:
        questions = PartSixProf()
        title = "Объектная модель прикладного решения"
    elif ERP:
        questions = PartSixErp()
        title = "Складское хозяйство"

    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)
  

@app.route('/part_seven', methods=['GET', 'POST'])
def part_seven():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    
    url = "part_seven"

    if PROF:
        questions = PartSevenProf()
        title = "Табличная модель прикладного решения"
    elif ERP:
        questions = PartSevenErp()
        title = "Продажи"
    
    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_eight', methods=['GET', 'POST'])
def part_eight():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    
    url = "part_eight"

    if PROF:
        questions = PartEightProf()
        title = "Механизмы интеграции и обмена данными"
    elif ERP:
        questions = PartEightErp()
        title = "Казначейство"

    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)
 

@app.route('/part_nine', methods=['GET', 'POST'])
def part_nine():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    url = "part_nine"

    if PROF:
        questions = PartNineProf()
        title = "Система взаимодействия"
    elif ERP:
        questions = PartNineErp()
        title = "Ведение взаиморасчетов"

    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_ten', methods=['GET', 'POST'])
def part_ten():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    url = "part_ten"

    if PROF:
        questions = PartTenProf()
        title = "Интерфейсные механизмы"
    elif ERP:
        questions = PartTenErp()
        title = "Нормирование"

    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)    
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_eleven', methods=['GET', 'POST'])
def part_eleven():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    url = "part_eleven"

    if PROF:
        questions = PartElevenProf()
        title = "Механизмы построения отчетности"
    elif ERP:
        questions = PartElevenErp()
        title = "Управление производством"

    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)    
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_twelve', methods=['GET', 'POST'])
def part_twelve():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    url = "part_twelve"

    if PROF:
        questions = PartTwelveProf()
        title = "Механизмы оперативного учета"
    elif ERP:
        questions = PartTwelveErp()
        title = "Производство"

    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)    
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_thirteen', methods=['GET', 'POST'])
def part_thirteen():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    url = "part_thirteen"

    if PROF:
        questions = PartThirteenProf()
        title = "Объекты и механизмы бухгалтирского учета"
    elif ERP:
        questions = PartThirteenErp()
        title = "Оперативный учет"

    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_fourteen', methods=['GET', 'POST'])
def part_fourteen():
    global COUNT, FLAG, ADMIN, USER, PROF, ERP
    FLAG = True
    
    
    url = "part_fourteen"

    if PROF:
        questions = PartFourteenProf()
        title = "Механизмы сложных переодических расчетов"
    elif ERP:
        questions = PartFourteenErp()
        title = "Регламентированный учет"

    if request.method == 'POST':
        if request.form["toBack"] == 'True':
            context = study_for_parts(title, url, questions, back_flag = True)
        else:
            context = study_for_parts(title, url, questions)   
    else:
        context = get_context(title, questions, url, True, True, False)
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/out')
def out():
    global ADMIN, USER
    out = Online()
    ADMIN = False
    USER = False
    out.change_params(ADMIN, USER)
    
    context = {
        "title": "1c",
        "flag": False,
        "admin": ADMIN,
        "user": USER,
    }
    
    return render_template('login.html', context=context)

    
if __name__ == '__main__':
    write()
    Online().change_params(False, False)
    ADMIN = False if int(params["admin"]) == 0 else  True
    USER = False if int(params["user"]) == 0 else True
    app.run(debug=False, port=5000)
    
    
  