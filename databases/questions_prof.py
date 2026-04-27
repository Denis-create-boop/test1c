import sqlite3


class QuestionsProf:
    """Класс который хранит в базе данных вопросы и варианты ответов"""
    
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/all_questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS questions_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """SELECT MAX(id) FROM questions_prof"""
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO questions_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """ UPDATE questions_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=?, f=?, image=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, f, image, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM questions_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM questions_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM questions_prof """
        self.cursor.execute(query)
        self.db.commit()
 
 
class PartsProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/parts_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS parts_prof (id INTEGER, text TEXT, url TEXT) """
            self.cursor.execute(query)
            self.db.commit()  
    
    
    def get_last_id(self):
        self.create_table()
        query = """ SELECT MAX(id) FROM parts_prof """
        self.cursor.execute(query)
        last_id = 0
        for row in self.cursor:
            if row[0] is not None:
                last_id = row[0]
        return last_id
        
                
    def write(self, text, path):
        self.create_table()
        last_id = self.get_last_id()
        self.id = last_id + 1
        
        query = """INSERT INTO parts_prof (id, text, url) VALUES (?, ?, ?)"""
        insert_payments = [
            (self.id, text, path),
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    def get_parts(self):
        self.create_table()
        
        query = """ SELECT * FROM parts_prof """
        self.cursor.execute(query)
        parts = {}
        count = 1
        for row in self.cursor:
            part = {}
            part["text"] = row[1]
            part["url"] = row[2] 
            parts[count] = part
            count += 1
            
        return parts 
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM parts_prof """ 
        self.cursor.execute(query)
        self.db.commit()
        
        
class PartOneProf:
    
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_one_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """SELECT MAX(id) FROM part_one_prof"""
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_one_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_one_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_one_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_one_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_one_prof """
        self.cursor.execute(query)
        self.db.commit()
    
       
class PartTwoProf:
    
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_two_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_two_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_two_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_two_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_two_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_two_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_two_prof """
        self.cursor.execute(query)
        self.db.commit()


class PartThreeProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_three_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_three_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_three_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_three_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_three_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_three_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_three_prof """
        self.cursor.execute(query)
        self.db.commit()
    

class PartFourProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_four_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_four_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_four_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_four_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_four_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_four_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_four_prof """
        self.cursor.execute(query)
        self.db.commit()
    

class PartFiveProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_five_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_five_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_five_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_five_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_five_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_five_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_five_prof """
        self.cursor.execute(query)
        self.db.commit()
    

class PartSixProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_six_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_six_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_six_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_six_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_six_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_six_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_six_prof """
        self.cursor.execute(query)
        self.db.commit()
    

class PartSevenProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_seven_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_seven_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_seven_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_seven_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_seven_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_seven_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_seven_prof """
        self.cursor.execute(query)
        self.db.commit()
    

class PartEightProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_eight_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_eight_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_eight_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_eight_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_eight_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_eight_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_eight_prof """
        self.cursor.execute(query)
        self.db.commit()
  
  
class PartNineProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_nine_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_nine_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
     
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_nine_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_nine_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_nine_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_nine_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_nine_prof """
        self.cursor.execute(query)
        self.db.commit()


class PartTenProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_ten_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_ten_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_ten_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_ten_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_ten_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_ten_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_ten_prof """
        self.cursor.execute(query)
        self.db.commit()


class PartElevenProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_eleven_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_eleven_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_eleven_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_eleven_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_eleven_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_eleven_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_eleven_prof """
        self.cursor.execute(query)
        self.db.commit()


class PartTwelveProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_twelve_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_twelve_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_twelve_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_twelve_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_twelve_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_twelve_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_twelve_prof """
        self.cursor.execute(query)
        self.db.commit()


class PartThirteenProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_thirteen_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_thirteen_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_thirteen_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_thirteen_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_thirteen_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_thirteen_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_thirteen_prof """
        self.cursor.execute(query)
        self.db.commit()
    
    
class PartFourteenProf:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/prof/questions_prof.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_fourteen_prof (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_fourteen_prof """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_fourteen_prof (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_fourteen_prof SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_fourteen_prof """
        self.cursor.execute(query)
        questions = {}
        count = 1
        for row in self.cursor:
            questions[count] = {"id": row[0], 
                         "question": row[1], 
                         "answer": row[2], 
                         "a": row[3], 
                         "b": row[4], 
                         "c": row[5], 
                         "d": row[6], 
                         "e": row[7],
                         "f": row[8],
                         "image": row[9]}
            count += 1
        return questions
    
    
    def get_question(self, id):
        """функция для получения конкретного вопроса"""
        self.create_table()
        query = """ SELECT * FROM part_fourteen_prof WHERE id=? """
        self.cursor.execute(query, (id,))
        question = {}
        
        for row in self.cursor:
            question['id'] = row[0]
            question['question'] = row[1]
            question['answer'] = row[2]
            question['a'] = row[3]
            question['b'] = row[4]
            question['c'] = row[5]
            question['d'] = row[6]
            question['e'] = row[7]
            question['f'] = row[8]
            question['image'] = row[9]
            
        return question
    
    
    def clean(self):
        self.create_table()
        query = """ DELETE FROM part_fourteen_prof """
        self.cursor.execute(query)
        self.db.commit()
   
 
