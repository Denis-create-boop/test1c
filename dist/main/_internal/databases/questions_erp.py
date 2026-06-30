import sqlite3


class QuestionsErp:
    """Класс который хранит в базе данных вопросы и варианты ответов"""
    
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('all_questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS questions_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """SELECT MAX(id) FROM questions_Erp"""
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO questions_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """ UPDATE questions_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=?, f=?, image=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, f, image, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM questions_Erp """
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
        query = """ SELECT * FROM questions_Erp WHERE id=? """
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
        query = """ DELETE FROM questions_Erp """
        self.cursor.execute(query)
        self.db.commit()
 
 
class PartsErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('parts_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS parts_Erp (id INTEGER, text TEXT, url TEXT) """
            self.cursor.execute(query)
            self.db.commit()  
     
    def get_last_id(self):
        self.create_table()
        query = """ SELECT MAX(id) FROM parts_erp """
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
        
        query = """INSERT INTO parts_Erp (id, text, url) VALUES (?, ?, ?)"""
        insert_payments = [
            (self.id, text, path),
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    def get_parts(self):
        self.create_table()
        
        query = """ SELECT * FROM parts_Erp """
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
        query = """ DELETE FROM parts_Erp """ 
        self.cursor.execute(query)
        self.db.commit()
        
        
class PartOneErp:
    
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_one_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """SELECT MAX(id) FROM part_one_Erp"""
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_one_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_one_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_one_Erp """
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
        query = """ SELECT * FROM part_one_Erp WHERE id=? """
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
        query = """ DELETE FROM part_one_Erp """
        self.cursor.execute(query)
        self.db.commit()
    
       
class PartTwoErp:
    
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_two_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_two_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_two_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_two_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_two_Erp """
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
        query = """ SELECT * FROM part_two_Erp WHERE id=? """
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
        query = """ DELETE FROM part_two_Erp """
        self.cursor.execute(query)
        self.db.commit()


class PartThreeErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_three_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_three_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_three_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_three_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_three_Erp """
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
        query = """ SELECT * FROM part_three_Erp WHERE id=? """
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
        query = """ DELETE FROM part_three_Erp """
        self.cursor.execute(query)
        self.db.commit()
    

class PartFourErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_four_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_four_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_four_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_four_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_four_Erp """
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
        query = """ SELECT * FROM part_four_Erp WHERE id=? """
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
        query = """ DELETE FROM part_four_Erp """
        self.cursor.execute(query)
        self.db.commit()
    

class PartFiveErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_five_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_five_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_five_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_five_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_five_Erp """
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
        query = """ SELECT * FROM part_five_Erp WHERE id=? """
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
        query = """ DELETE FROM part_five_Erp """
        self.cursor.execute(query)
        self.db.commit()
    

class PartSixErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_six_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_six_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_six_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_six_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_six_Erp """
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
        query = """ SELECT * FROM part_six_Erp WHERE id=? """
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
        query = """ DELETE FROM part_six_Erp """
        self.cursor.execute(query)
        self.db.commit()
    

class PartSevenErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_seven_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_seven_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_seven_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_seven_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_seven_Erp """
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
        query = """ SELECT * FROM part_seven_Erp WHERE id=? """
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
        query = """ DELETE FROM part_seven_Erp """
        self.cursor.execute(query)
        self.db.commit()
    

class PartEightErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_eight_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_eight_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_eight_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_eight_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_eight_Erp """
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
        query = """ SELECT * FROM part_eight_Erp WHERE id=? """
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
        query = """ DELETE FROM part_eight_Erp """
        self.cursor.execute(query)
        self.db.commit()
  
  
class PartNineErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_nine_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_nine_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
     
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_nine_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_nine_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_nine_Erp """
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
        query = """ SELECT * FROM part_nine_Erp WHERE id=? """
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
        query = """ DELETE FROM part_nine_Erp """
        self.cursor.execute(query)
        self.db.commit()


class PartTenErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_ten_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_ten_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_ten_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_ten_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_ten_Erp """
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
        query = """ SELECT * FROM part_ten_Erp WHERE id=? """
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
        query = """ DELETE FROM part_ten_Erp """
        self.cursor.execute(query)
        self.db.commit()


class PartElevenErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_eleven_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_eleven_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_eleven_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_eleven_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_eleven_Erp """
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
        query = """ SELECT * FROM part_eleven_Erp WHERE id=? """
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
        query = """ DELETE FROM part_eleven_Erp """
        self.cursor.execute(query)
        self.db.commit()


class PartTwelveErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_twelve_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_twelve_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_twelve_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_twelve_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_twelve_Erp """
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
        query = """ SELECT * FROM part_twelve_Erp WHERE id=? """
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
        query = """ DELETE FROM part_twelve_Erp """
        self.cursor.execute(query)
        self.db.commit()


class PartThirteenErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_thirteen_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_thirteen_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_thirteen_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_thirteen_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_thirteen_Erp """
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
        query = """ SELECT * FROM part_thirteen_Erp WHERE id=? """
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
        query = """ DELETE FROM part_thirteen_Erp """
        self.cursor.execute(query)
        self.db.commit()
    
    
class PartFourteenErp:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('questions_Erp.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS part_fourteen_Erp (id INTEGER, question TEXT, answer TEXT, a TEXT, b TEXT, c TEXT, d TEXT, e TEXT, f TEXT, image TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def get_last_id(self):
        """функция для получения последнего id"""
        self.create_table()
        query = """ SELECT MAX(id) FROM part_fourteen_Erp """
        self.cursor.execute(query)
        for row in self.cursor:
            if  row[0]:
                self.id = int(row[0]) + 1
        return self.id - 1
        
    
    
    def add_question(self, question, answer, a, b, c, d=None, e=None, f=None, image=None):
        """функция для добавления вопроса в бд"""
        self.create_table()
        self.get_last_id()
        query = """INSERT INTO part_fourteen_Erp (id, question, answer, a, b, c, d, e, f, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_payments = [
            (self.id, question, answer, a, b, c, d, e, f, image,)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        
    
    def change_question(self, id, question, answer, a, b, c, d=None, e=None):
        """функция для измениния вопроса либо вариантов ответа"""
        self.create_table()
        query = """UPDATE part_fourteen_Erp SET question=?, answer=?, a=?, b=?, c=?, d=?, e=? WHERE id=? """
        insert_payments = [
            (question, answer, a, b, c, d, e, id)
        ]
        self.cursor.executemany(query, insert_payments)
        self.db.commit()
        

    def get_all_questions(self):
        """функция для получения всех вопросов из бд"""
        self.create_table()
        query = """ SELECT * FROM part_fourteen_Erp """
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
        query = """ SELECT * FROM part_fourteen_Erp WHERE id=? """
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
        query = """ DELETE FROM part_fourteen_Erp """
        self.cursor.execute(query)
        self.db.commit()
   
  