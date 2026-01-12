from admin import *
from databases.start_questions import *
import random


QUESTIONS = []
ANSWERS_LIST = []
COUNT = 1
FLAG = False
EXAM_COUNT = 0


part_list = [PartOne(), PartTwo(), PartThree(), PartFour(), PartFive(), PartSix(), PartSeven(), PartEight(), PartNine(), PartTen(), PartEleven(), 
            PartTwelve(), PartThirteen(), PartFourteen()]


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
        all_questions = questions.get_all_question()
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
 
 
def write():
    
    data = {1: {"path": "./questions/part_one.txt", "db": PartOne()},
            2: {"path": "./questions/part_two.txt", "db": PartTwo()},
            3: {"path": "./questions/part_three.txt", "db": PartThree()},
            4: {"path": "./questions/part_four.txt", "db": PartFour()},
            5: {"path": "./questions/part_five.txt", "db": PartFive()},
            6: {"path": "./questions/part_six.txt", "db": PartSix()},
            7: {"path": "./questions/part_seven.txt", "db": PartSeven()},
            8: {"path": "./questions/part_eight.txt", "db": PartEight()},
            9: {"path": "./questions/part_nine.txt", "db": PartNine()},
            10: {"path": "./questions/part_ten.txt", "db": PartTen()},
            11: {"path": "./questions/part_eleven.txt", "db": PartEleven()},
            12: {"path": "./questions/part_twelve.txt", "db": PartTwelve()},
            13: {"path": "./questions/part_thirteen.txt", "db": PartThirteen()},
            14: {"path": "./questions/part_fourteen.txt", "db": PartFourteen()}}
    for k, v in data.items():
        if v["db"].get_last_id():
            continue
        else:
            write_to_db(v["path"], v["db"])
 
 
def get_context(title, questions, url, flag, first_question, last_question):
    global ADMIN, USER, COUNT

    all_questions = questions.get_all_question()
    
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
    global COUNT, QUESTIONS, EXAM_COUNT, ANSWERS_LIST, ADMIN, USER, params
    
    ADMIN = False if int(params["admin"]) == 0 else  True
    USER = False if int(params["user"]) == 0 else True
    
    create_account(flag=True)
    create_account()
    
    QUESTIONS = []
    EXAM_COUNT = 0
    ANSWERS_LIST = []
    COUNT = 1
    
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

        }
        if ADMIN or USER:
            return render_template('index.html', context=context)
        else:
            return render_template('login.html', context=context)


@app.route('/test')
def test():
    global QUESTIONS, FLAG, COUNT, ADMIN, USER, part_list
    COUNT = 1
    FLAG = False

    questions = Questions()
    last_id = questions.get_last_id()
    
    for part in part_list:
        last_id = part.get_last_id()
        number = random.randrange(1, last_id)
        question = part.get_question(number)
        QUESTIONS.append(question)
        random.shuffle(QUESTIONS)
    
    context = {
        "title": "Экзамен",
        'url': 'test_quest',
        "admin": ADMIN,
        "user": USER,
    }

    
    return render_template('test.html', context=context)
    
@app.route('/test_with_answers') 
def test_with_answers():
    global QUESTIONS, FLAG, COUNT, ADMIN, USER, part_list
    COUNT = 1
    FLAG = True
    QUESTIONS = []

    questions = Questions()
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
    global QUESTIONS, FLAG, COUNT, ADMIN, USER, ANSWERS_LIST

    title = "Экзамен"
    url = "test_quest"
    context = None
    
    def misstakes():
        ANSWERS_LIST.append(request.form['answer'])
        COUNT = 0
        answers = 0
        misstakes = 0
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
        
        for question in QUESTIONS:
            if question['answer'] == ANSWERS_LIST[COUNT]:
                answers += 1
                COUNT += 1
            else:
                misstakes += 1
                COUNT += 1
        if misstakes > 2:
            result = f"Тест не сдан вы совершили {misstakes} {misstake_dict[misstakes]}"
        else:
            result = f"Поздровляем тест сдан вы совершили {misstakes} {misstake_dict[misstakes]}"
        COUNT = 0   

        context = {
            "title": "Результат",
            "result": result,
            "misstakes": misstakes,
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
                        question = QUESTIONS[COUNT - 1]
                        question["id"] = COUNT
                        context = {
                            "question": question,
                            "flag": FLAG,
                            'url': url,
                            "title": title,
                            "first_question": False,
                            "last_question": False,
                            "admin": ADMIN,
                            "user": USER,
                        }
                        COUNT += 1
                except:
                        ANSWERS_LIST.append(request.form['answer'])
                        question = QUESTIONS[COUNT - 1]
                        question["id"] = COUNT
                        context = {
                            "question": question,
                            "flag": FLAG,
                            'url': url,
                            "title": title,
                            "first_question": False,
                            "last_question": False,
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
    global COUNT, ADMIN, USER
    COUNT = 1

    context = {
        'questions': {
            1: {'text': '1 общие механизмы, понятия и термины', 'url': 'part_one'},
            2: {'text': '2 Редакторы и инструменты общие', 'url': 'part_two'},
            3: {'text': '3 Редакторы и инструменты режима разработки', 'url': 'part_three'},
            4: {'text': '4 Конструкторы', 'url': 'part_four'},
            5: {'text': '5 Технология разработки', 'url': 'part_five'},
            6: {'text': '6 Объектная модель прикладного решения', 'url': 'part_six'},
            7: {'text': '7 Табличная модель прикладного решения', 'url': 'part_seven'},
            8: {'text': '8 Механизмы интеграции и обмена данными', 'url': 'part_eight'},
            9: {'text': '9 Система взаимодействия', 'url': 'part_nine'},
            10: {'text': '10 Интерфейсные механизмы', 'url': 'part_ten'},
            11: {'text': '11 Механизмы построения отчетности', 'url': 'part_eleven'},
            12: {'text': '12 Механизмы оперативного учета', 'url': 'part_twelve'},
            13: {'text': '13 Объекты и механизмы бухгалтирского учета', 'url': 'part_thirteen'},
            14: {'text': '14 Механизмы сложных переодических расчетов', 'url': 'part_fourteen'}
        },
        'flag': True,
        "admin": ADMIN,
        "user": USER,
    }
    
    
    return render_template('parts.html', context= context)
 
 
@app.route('/part_one', methods=['GET', 'POST'])
def part_one():
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "общие механизмы, понятия и термины"
    url = "part_one"
    
    questions = PartOne()
    
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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Редакторы и инструменты общие"
    url = "part_two"
    
    questions = PartTwo() 
    
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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Редакторы и инструменты режима разработки"
    url = "part_three"

    questions = PartThree()
    
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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Конструкторы"
    url = "part_four"

    questions = PartFour()
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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Технология разработки"
    url = "part_five"

    questions = PartFive()
    
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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Объектная модель прикладного решения"
    url = "part_six"

    questions = PartSix()

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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Табличная модель прикладного решения"
    url = "part_seven"

    questions = PartSeven()
    
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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Механизмы интеграции и обмена данными"
    url = "part_eight"

    questions = PartEight()

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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Система взаимодействия"
    url = "part_nine"

    questions = PartNine()

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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Интерфейсные механизмы"
    url = "part_ten"

    questions = PartTen()

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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Механизмы построения отчетности"
    url = "part_eleven"

    questions = PartEleven()

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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Механизмы оперативного учета"
    url = "part_twelve"

    questions = PartTwelve()

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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Объекты и механизмы бухгалтирского учета"
    url = "part_thirteen"

    questions = PartThirteen()

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
    global COUNT, FLAG, ADMIN, USER
    FLAG = True
    
    title = "Механизмы сложных переодических расчетов"
    url = "part_fourteen"

    questions = PartFourteen()

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
    
    
  