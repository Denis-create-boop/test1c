from admin import *
from databases.start_questions import *
import random


    
QUESTIONS = []
REPEAT_QUESTIONS = []
ANSWERS_LIST = []
COUNT = 1
FLAG = False


def study_for_parts(title, url, questions):
    global COUNT, FLAG
    FLAG = True
    all_questions = questions.get_all_question()
    if all_questions[COUNT]:
        if COUNT == questions.get_last_id():
            context = {
                "title": title,
                "question": all_questions[COUNT],
                "url": url,
                "flag": True,
                "last_question": True
            }
            COUNT = 1
        else:
            context = {
                "title": title,
                "question": all_questions[COUNT],
                'url': url,
                'flag': True,
                'last_question': False,
            }
            COUNT += 1
    return context
    
    
@app.route('/', methods=['GET', 'POST'])
def index():
    global COUNT
    COUNT = 1
    if request.method == 'POST':
        context = {
            'title': '1c', 
            'flag': True,
        }
    else:
        context = {
            'title': '1c', 
            'flag': False,
        }
    return render_template('index.html', context=context)


@app.route('/test')
def test():
    global QUESTIONS, REPEAT_QUESTIONS, FLAG, COUNT
    COUNT = 1
    FLAG = False
    questions = Questions()
    last_id = questions.get_last_id()
    while len(QUESTIONS) < 14:
        number = random.randrange(1, last_id+1)
        if number not in QUESTIONS:
            QUESTIONS.append(number)
    REPEAT_QUESTIONS = QUESTIONS
    context = {
        "title": "test",
        'url': 'test_quest',
    }
    
    return render_template('test.html', context=context)
    
@app.route('/test_with_answers') 
def test_with_answers():
    global QUESTIONS, REPEAT_QUESTIONS, FLAG, COUNT
    COUNT = 1
    FLAG = True
    questions = Questions()
    last_id = questions.get_last_id()
    while len(QUESTIONS) < 14:
        number = random.randrange(1, last_id+1)
        if number not in QUESTIONS:
            QUESTIONS.append(number)
    REPEAT_QUESTIONS = QUESTIONS
    context = {
        "title": "with_answers",
        'url': 'test_quest',
    }
    
    return render_template('test.html', context=context)
 
    
@app.route('/test_quest', methods=['GET', "POST"])
def test_quest():
    global QUESTIONS, FLAG, COUNT
    COUNT = 1
    
    if len(QUESTIONS) > 0:
        if request.method == 'POST':
            ANSWERS_LIST.append(request.form['answer'])
            id = QUESTIONS[0]
            one_question = Questions().get_question(id=id)
            print(one_question)
            if len(QUESTIONS) == 1:
                QUESTIONS = []
            else:
                QUESTIONS = QUESTIONS[1:]
                
            context = {
                "question": one_question,
                'flag': FLAG,
                'url': 'test_quest',
            }

        else:
            id = QUESTIONS[0]
            one_question = Questions().get_question(id=id)
            QUESTIONS = QUESTIONS[1:]
            context = {
                "question": one_question,
                "flag": FLAG,
                'url': 'test_quest',
            }
        
        return render_template('test.html', context=context)
    else:
        ANSWERS_LIST.append(request.form['answer'])
        answers = 0
        misstakes = 0
        misstake_dict = {
            1: "ошибку",
            2: "ошибки",
            3: "ошибки",
            4: "ошибки",
            5: "ошибок",
            6: "ошибок",
            7: "ошибок",
            8: "ошибок",
            9: "ошибок",
            10: "ошибок"
        }
        for i in range(len(REPEAT_QUESTIONS)):

            if Questions().get_question(REPEAT_QUESTIONS[i])['answer'] == ANSWERS_LIST[i]:
                answers += 1
            else:
                misstakes += 1
        if misstakes > 2:
            result = f"Тест не пройден вы совершили {misstakes} {misstake_dict[misstakes]}"
        else:
            result = "Поздровляем тест сдан"
            
        context = {
            "title": "result",
            "result": result,
            "misstakes": misstakes,
        }
        
        return render_template('result.html', context=context)


@app.route('/show_misstakes')
def show_misstakes():
    global REPEAT_QUESTIONS, ANSWERS_LIST
    question = Questions().get_question(REPEAT_QUESTIONS[0])
    REPEAT_QUESTIONS = REPEAT_QUESTIONS[1:]
    answer = ANSWERS_LIST[0]
    ANSWERS_LIST = ANSWERS_LIST[1:]
    if len(REPEAT_QUESTIONS) > 0:
        url = 'show_misstakes'
        message = "Следующий вопрос"
    else:
        url = 'index'
        message = "На главную"
    context = {
        "title": "show misstakes",
        "question": question,
        "answer": answer,
        "url": url,
        "message": message
    }

    return render_template('answers.html', context=context)


@app.route('/study')
def study():
    global COUNT
    COUNT = 1
    context = {
        'questions': {
            1: {'text': '1 общие механизмы, понятия и термины', 'url': 'part_one'},
            2: {'text': '2 Редакторы и инструменты общие', 'url': 'part_two'},
            3: {'text': '3 Редакторы и инструменты режима разработки', 'url': 'part_three'},
            4: {'text': '4 Конструкторы', 'url': 'part_four'},
            5: {'text': '5 Технология разработки', 'url': 'part_five'},
            6: {'text': '6 Объектная модель прикладного решения', 'url': ''},
            7: {'text': '7 Табличная модель прикладного решения', 'url': ''},
            8: {'text': '8 Механизмы интеграции и обмена данными', 'url': ''},
            9: {'text': '9 Система взаимодействия', 'url': ''},
            10: {'text': '10 Интерфейсные механизмы', 'url': ''},
            11: {'text': '11 Механизмы построения отчетности', 'url': ''},
            12: {'text': '12 Механизмы оперативного учета', 'url': ''},
            13: {'text': '13 Объекты и механизмы бухгалтирского учета', 'url': ''},
            14: {'text': '14 Механизмы сложных переодических расчетов', 'url': ''}
        },
        'flag': True,
    }
    
    
    return render_template('parts.html', context= context)
 
 
@app.route('/part_one', methods=['GET', 'POST'])
def part_one():
    global COUNT, FLAG
    FLAG = True
    questions = PartOne()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("part_one", "part_one", questions)
    else:
        context = {
            "title": "part_one",
            "question": all_questions[COUNT],
            "url": "part_one",
            "flag": True,
            "last_question": False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)
 
 
@app.route('/part_two', methods=['GET', 'POST'])
def part_two():
    global COUNT, FLAG
    FLAG = True
    questions = PartTwo()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("part_two", "part_two", questions)    
    else:
        context = {
            "title": "part_two",
            "question": all_questions[COUNT],
            "url": "part_two",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_three', methods=['GET', 'POST'])
def part_three():
    global COUNT, FLAG
    FLAG = True
    questions = PartThree()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("part_three", "part_three", questions)    
    else:
        context = {
            "title": "part_three",
            "question": all_questions[COUNT],
            "url": "part_three",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)
 
 
@app.route('/part_four', methods=['GET', 'POST'])
def part_four():
    global COUNT, FLAG
    FLAG = True
    COUNT = 52
    questions = PartFour()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("part_four", "part_four", questions)    
    else:
        context = {
            "title": "part_four",
            "question": all_questions[COUNT],
            "url": "part_four",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_five', methods=['GET', 'POST'])
def part_five():
    global COUNT, FLAG
    FLAG = True
    questions = PartFive()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("part_five", "part_five", questions)    
    else:
        context = {
            "title": "part_five",
            "question": all_questions[COUNT],
            "url": "part_five",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)

    
if __name__ == '__main__':
    id = Questions().get_last_id()
    if id:
        app.run()
    else:
        data = {1: {"path": "./questions/part_one.txt", "db": PartOne()},
                2: {"path": "./questions/part_two.txt", "db": PartTwo()},
                3: {"path": "./questions/part_three.txt", "db": PartThree()},
                4: {"path": "./questions/part_four.txt", "db": PartFour()},
                5: {"path": "./questions/part_five.txt", "db": PartFive()}}
        for k, v in data.items():
            write_to_db(v["path"], v["db"])

        app.run()