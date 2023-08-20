import sqlite3

class UsersDatabase:
    def __init__(self, db_name='../databases/user_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY);')
        self.conn.commit()

    def add_user(self, user_id):
        self.cursor.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        self.conn.commit()

    def user_exists(self, user_id):
        self.cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone() is not None

    def get_all_entries(self):
        self.cursor.execute('SELECT * FROM users;')
        return self.cursor.fetchall()
    def close(self):
        self.cursor.close()
        self.conn.close()
