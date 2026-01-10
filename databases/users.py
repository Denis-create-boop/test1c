import sqlite3


class Users:
    
    def __init__(self):
        self.db = None
        self.cursor = None
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('./databases/users.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS users (login Text, password Text, is_admin TEXT) """
            self.cursor.execute(query)
            self.db.commit()
            
            
    def add_user(self, new_login, new_password, admin, flag=False):
        self.create_table()
        if flag:
            query = f""" SELECT * FROM users WHERE login='{new_login}' """
            self.cursor.execute(query)
            is_user = False
            for row in self.cursor:
                is_user = True
            if is_user:
                return
            else:
                query = """ INSERT INTO users (login, password, is_admin) VALUES(?, ?, ?) """
                self.cursor.executemany(query, [(new_login, new_password, admin,)])
                self.db.commit()
        
        else:
            query = """ SELECT * FROM users WHERE is_admin=1 """
            self.cursor.execute(query)
            is_admin = False
            for row in self.cursor:
                is_admin = True
            if is_admin:
                return
            else:
                query = """ INSERT INTO users (login, password, is_admin) VALUES (?, ?, ?) """
                self.cursor.executemany(query, [(new_login, new_password, admin,)])
                self.db.commit()


            
            
    def get_login_and_password(self, send_login):
        self.create_table()
        str_query = f""" SELECT * FROM users WHERE login='{send_login}' """
        query = str_query
        self.cursor.execute(query)
        data = dict()
        for row in self.cursor:
            data["login"] = row[0]
            data["password"] = row[1]
            data["admin"] = row[2]
            
        return data
    
    def get_all(self):
        self.create_table()
        quesry = """ SELECT * FROM users """
        self.cursor.execute(quesry)
        data = []
        for row in self.cursor:
            data.append(row)
            
        return data
            
    


