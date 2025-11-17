# Em task_repository.py
# (Exemplo com sqlite3)
import sqlite3
from models.task import Task

class TaskRepository:
    def __init__(self, db_path='taskflow.db'):
        self.db_path = db_path
        # (Você também precisará de um método para criar a tabela)

    def add(self, task):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
            (task.title, task.description, task.status)
        )
        conn.commit()
        
        task.id = cursor.lastrowid # Pega o ID que o DB gerou
        conn.close()
        
        return task