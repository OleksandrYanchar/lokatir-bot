import sqlite3

class QuizDatabase:
    def __init__(self, db_name='quiz_database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                score INTEGER
            )
        ''')
        self.conn.commit()

    def save_quiz_result(self, user_id, username, score):
        self.cursor.execute('INSERT INTO quiz_results (user_id, username, score) VALUES (?, ?, ?)',
                            (user_id, username, score))
        self.conn.commit()

    def get_top_result(self):
        self.cursor.execute('SELECT username, score FROM quiz_results ORDER BY score DESC LIMIT 1')
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
