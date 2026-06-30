from databases.questions_prof import *
from databases.questions_erp import *
from databases.users import Users
from admin import resource_path


def write_to_db_questions(PATH, db, exam):
     """Фукция для заполнения базы данных если она пуста"""
     questions = dict()
     number = 1
     step = 0
     flag = False
     with open(PATH, 'r', encoding='utf-8') as file:
          list_variants = ['question', 'a', 'b', 'c', 'd', 'e', 'f', 'answer', 'image']
          for line in file.readlines():
               if step < 9:
                    if not flag:
                         questions[number] = dict()
                         flag = True
                    if step == 0:     
                         start = line.find(' ')
                    elif step == 8:
                         start = 0
                    else:
                         start = line.find('.')
                         start += 1
                    questions[number][list_variants[step]] = line[start:].rstrip()
                    step += 1
                    if step == 9:
                         step = 0
                         number += 1
                         flag = False
     if exam == "prof":                    
          write = QuestionsProf()
     elif exam == "erp":
          write = QuestionsErp()

     
     for key, value in questions.items():
          write.add_question(value['question'], value['answer'], value['a'], value['b'], value['c'], value['d'], value['e'], value['f'], value['image'])         
          db.add_question(value['question'], value['answer'], value['a'], value['b'], value['c'], value['d'], value['e'], value['f'], value['image'])  


def write_to_db_parts(parts, db):
     
     for k, v in parts.items():
          db.write(v["text"], v["url"])
               

def create_account(flag=False):
     main_user = Users()
     if flag:
          
          with open(resource_path("./databases/gets_some_instruments.txt"), "r") as file:
              user = file.read().split("\n")

          user_login = user[0].split(', ')
          user_password = user[1].split(', ')

          LOGIN = ""
          PASSWORD = ""

          for number in user_login:
              LOGIN += chr(int(number))

          for number in user_password:
              PASSWORD += chr(int(number))
          
          main_user.add_user(LOGIN, PASSWORD, True)
          main_user.add_user("Andrey", "12345")
          main_user.add_user("Alecsey", "12345")
     else:
         pass
        