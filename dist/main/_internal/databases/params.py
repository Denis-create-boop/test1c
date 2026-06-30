import sqlite3 


class Online:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.id = 1
        
    
    def create_table(self):
        """функция для создания таблицы"""
        with sqlite3.connect('params.db') as db:
            self.db = db
            self.cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS params (admin, TEXT, user TEXT) """
            self.cursor.execute(query)
            self.db.commit()
        self.write()
    
    def write(self):
        query = """ SELECT * FROM params """
        self.cursor.execute(query)
        flag = None
        for row in self.cursor:
            flag = row
        
        if flag is None:
            query = """ INSERT INTO params (admin, user) VALUES (False, False) """
            self.cursor.execute(query)
            self.db.commit()
        else:
            return
    
    
    def get_params(self):
        self.create_table()
        query = """ SELECT * FROM params """    
        params = {}
        self.cursor.execute(query)
        for row in self.cursor:
            params["admin"] = row[0]
            params["user"] = row[2]
        
        return params
    
    def change_params(self, new_admin, new_user):
        self.create_table()
        query = f""" UPDATE params SET admin={new_admin}, user={new_user} """
        self.cursor.execute(query)
        self.db.commit()
    

