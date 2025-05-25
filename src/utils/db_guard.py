import sqlite3

class SqliteGuard:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
