import sqlite3


class DataBase:
    def __init__(self, db = "chatbot.db"):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.c = self.conn.cursor()

        self.c.execute("""CREATE TABLE IF NOT EXISTS chats(id INTEGER PRIMARY KEY AUTOINCREMENT,
     title TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    role TEXT,
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(chat_id) REFERENCES chats(id))""")
    def get_id(self, title):
        self.c.execute("INSERT INTO chats (title) VALUES (?)", (title,))
        self.conn.commit()
        chat_id = self.c.lastrowid
        return chat_id
    def storeUser(self, chat_id, user_text):
        self.c.execute("INSERT INTO messages (chat_id, role, content) VALUES (?,?,?)",
                  (chat_id, "user", user_text))
        self.conn.commit()
    def storeAI(self,chat_id, ai_text):
        self.c.execute("INSERT INTO messages (chat_id, role, content) VALUES (?,?,?)",
                  (chat_id, "assistant", ai_text))
        self.conn.commit()

    def load(self, chat_id):
        self.c.execute("SELECT role, content FROM messages WHERE chat_id = ? ORDER BY id",
                  (chat_id,))
        rows = self.c.fetchall()
        return rows
    def load_titles(self):
        self.c.execute("SELECT title FROM chats ORDER BY created_at")
        titles = self.c.fetchall()
        return titles
    def delete_all(self):
        self.c.execute("DELETE FROM chats")
        self.c.execute("DELETE FROM messages")
    def load_all(self):
        self.c.execute("SELECT * FROM chats ORDER BY created_at DESC")
        stuff = self.c.fetchall()
        return stuff
db = DataBase()

