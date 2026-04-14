import sqlite3


class Database:
    def __init__(self, path: str = "sqlite.db"):
        self.path = path
        self.connection: sqlite3.Connection | None = None

    def connect(self):
        self.connection = sqlite3.connect(self.path)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
