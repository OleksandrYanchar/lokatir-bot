import sqlite3
from typing import List


class UsersDatabase:
    def __init__(self, db_name: str="../databases/user_data.db") -> None:
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY);")
        self.conn.commit()

    def add_user(self, user_id: int) -> None:
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        self.conn.commit()

    def user_exists(self, user_id: int) -> bool:
        self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone() is not None

    def get_all_entries(self) -> List[int]:
        self.cursor.execute("SELECT * FROM users;")
        return self.cursor.fetchall()

    def close(self) -> None:
        self.cursor.close()
        self.conn.close()
