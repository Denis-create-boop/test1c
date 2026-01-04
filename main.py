from admin import *
from databases.start_questions import *
import random


    
QUESTIONS = []
REPEAT_QUESTIONS = []
ANSWERS_LIST = []
COUNT = 1
FLAG = False
EXAM_COUNT = 0



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
 
 
def write():
    id = Questions().get_last_id()
    if id:
        return
    else:
        data = {1: {"path": "./questions/part_one.txt", "db": PartOne()},
                2: {"path": "./questions/part_two.txt", "db": PartTwo()},
                3: {"path": "./questions/part_three.txt", "db": PartThree()},
                4: {"path": "./questions/part_four.txt", "db": PartFour()},
                5: {"path": "./questions/part_five.txt", "db": PartFive()},
                6: {"path": "./questions/part_six.txt", "db": PartSix()},
                7: {"path": "./questions/part_seven.txt", "db": PartSeven()},
                8: {"path": "./questions/part_eight.txt", "db": PartEight()},}
            #    9: {"path": "./questions/part_nine.txt", "db": PartNine()},
            #    10: {"path": "./questions/part_ten.txt", "db": PartTen()},
            #    11: {"path": "./questions/part_eleven.txt", "db": PartEleven()},
            #    12: {"path": "./questions/part_twelve.txt", "db": PartTwelve()},
             #   13: {"path": "./questions/part_thirteen.txt", "db": PartThirteen()},
            #    14: {"path": "./questions/part_fourteen.txt", "db": PartFourteen()}}
        for k, v in data.items():
            write_to_db(v["path"], v["db"])
            
                  
    
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
    part_list = [PartOne(), PartTwo(), PartThree(), PartFour(), PartFive(), PartSix(), PartSeven(), PartEight(), PartNine(), PartTen(), PartEleven(), 
                 PartTwelve(), PartThirteen(), PartFourteen()]
    questions = Questions()
    last_id = questions.get_last_id()
    
    for part in part_list:
        last_id = part.get_last_id()
        number = random.randrange(1, last_id)
        question = part.get_question(number)
        QUESTIONS.append(question)

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
    global QUESTIONS, FLAG, COUNT, EXAM_COUNT
    COUNT = 1
    
    if len(QUESTIONS) > 0  and COUNT != 14:
        if request.method == 'POST':
            ANSWERS_LIST.append(request.form['answer'])
            one_question = QUESTIONS[EXAM_COUNT]
            EXAM_COUNT += 1
                
            context = {
                "question": one_question,
                'flag': FLAG,
                'url': 'test_quest',
            }

        else:
            one_question = QUESTIONS[EXAM_COUNT]
            EXAM_COUNT += 1
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
    }
    
    
    return render_template('parts.html', context= context)
 
 
@app.route('/part_one', methods=['GET', 'POST'])
def part_one():
    global COUNT, FLAG
    FLAG = True
    questions = PartOne()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("общие механизмы, понятия и термины", "part_one", questions)
    else:
        context = {
            "title": "общие механизмы, понятия и термины",
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
        context = study_for_parts("Редакторы и инструменты общие", "part_two", questions)    
    else:
        context = {
            "title": "Редакторы и инструменты общие",
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
        context = study_for_parts("Редакторы и инструменты режима разработки", "part_three", questions)    
    else:
        context = {
            "title": "Редакторы и инструменты режима разработки",
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
        context = study_for_parts("Конструкторы", "part_four", questions)    
    else:
        context = {
            "title": "Конструкторы",
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
        context = study_for_parts("Технология разработки", "part_five", questions)    
    else:
        context = {
            "title": "Технология разработки",
            "question": all_questions[COUNT],
            "url": "part_five",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_six', methods=['GET', 'POST'])
def part_six():
    global COUNT, FLAG
    FLAG = True
    questions = PartSix()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Объектная модель прикладного решения", "part_six", questions)    
    else:
        context = {
            "title": "Объектная модель прикладного решения",
            "question": all_questions[COUNT],
            "url": "part_six",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)
  


@app.route('/part_seven', methods=['GET', 'POST'])
def part_seven():
    global COUNT, FLAG
    FLAG = True
    questions = PartSeven()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Табличная модель прикладного решения", "part_seven", questions)    
    else:
        context = {
            "title": "Табличная модель прикладного решения",
            "question": all_questions[COUNT],
            "url": "part_seven",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_eight', methods=['GET', 'POST'])
def part_eight():
    global COUNT, FLAG
    FLAG = True
    questions = PartEight()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Механизмы интеграции и обмена данными", "part_eight", questions)    
    else:
        context = {
            "title": "Механизмы интеграции и обмена данными",
            "question": all_questions[COUNT],
            "url": "part_eight",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)
 

@app.route('/part_nine', methods=['GET', 'POST'])
def part_nine():
    global COUNT, FLAG
    FLAG = True
    questions = PartNine()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Система взаимодействия", "part_nine", questions)    
    else:
        context = {
            "title": "Система взаимодействия",
            "question": all_questions[COUNT],
            "url": "part_nine",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_ten', methods=['GET', 'POST'])
def part_ten():
    global COUNT, FLAG
    FLAG = True
    questions = PartTen()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Интерфейсные механизмы", "part_ten", questions)    
    else:
        context = {
            "title": "Интерфейсные механизмы",
            "question": all_questions[COUNT],
            "url": "part_ten",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_eleven', methods=['GET', 'POST'])
def part_eleven():
    global COUNT, FLAG
    FLAG = True
    questions = PartEleven()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Механизмы построения отчетности", "part_eleven", questions)    
    else:
        context = {
            "title": "Механизмы построения отчетности",
            "question": all_questions[COUNT],
            "url": "part_eleven",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_twelve', methods=['GET', 'POST'])
def part_twelve():
    global COUNT, FLAG
    FLAG = True
    questions = PartTwelve()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Механизмы оперативного учета", "part_twelve", questions)    
    else:
        context = {
            "title": "Механизмы оперативного учета",
            "question": all_questions[COUNT],
            "url": "part_twelve",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_thirteen', methods=['GET', 'POST'])
def part_thirteen():
    global COUNT, FLAG
    FLAG = True
    questions = PartThirteen()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Объекты и механизмы бухгалтирского учета", "part_thirteen", questions)    
    else:
        context = {
            "title": "Объекты и механизмы бухгалтирского учета",
            "question": all_questions[COUNT],
            "url": "part_thirteen",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


@app.route('/part_fourteen', methods=['GET', 'POST'])
def part_fourteen():
    global COUNT, FLAG
    FLAG = True
    questions = PartFourteen()
    all_questions = questions.get_all_question()
    if request.method == 'POST':
        context = study_for_parts("Механизмы сложных переодических расчетов", "part_fourteen", questions)    
    else:
        context = {
            "title": "Механизмы сложных переодических расчетов",
            "question": all_questions[COUNT],
            "url": "part_fourteen",
            "flag": True,
            'last_question': False,
        }
        COUNT += 1
    
    return render_template('test.html', context=context)


    
if __name__ == '__main__':
    write()
    app.run()
    
    
    