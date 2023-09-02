import os
import sqlite3
from typing import List, Tuple, Optional

class QuizDatabase:
    def __init__(self, db_name: str = "quiz_database.db") -> None:
        db_path = os.path.join(os.path.dirname(__file__), "../../databases", db_name)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quiz_results (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                score INTEGER
            )
        """
        )
        self.conn.commit()

    def save_quiz_result(self, user_id: int, username: str, score: int) -> None:
        self.cursor.execute("SELECT score FROM quiz_results WHERE user_id = ?", (user_id,))
        existing_score: Optional[Tuple[int]] = self.cursor.fetchone()

        if existing_score:
            if score > existing_score[0]:
                self.cursor.execute(
                    "UPDATE quiz_results SET username = ?, score = ? WHERE user_id = ?", (username, score, user_id)
                )
        else:
            self.cursor.execute(
                "INSERT INTO quiz_results (user_id, username, score) VALUES (?, ?, ?)", (user_id, username, score)
            )

        self.conn.commit()

    def get_top_results(self, limit: int = 10) -> List[Tuple[str, int]]:
        self.cursor.execute("SELECT username, score FROM quiz_results ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

    def close(self) -> None:
        self.conn.close()
