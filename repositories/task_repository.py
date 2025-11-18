import sqlite3
from models.task import Task
from .base_repository import BaseRepository

class TaskRepository(BaseRepository):
    def __init__(self, db_path="taskflow.db"):
        self.db_path = db_path

    def _get_connection(self):
        # Retorna uma nova conexão (SQLite prefere conexões por thread)
        return sqlite3.connect(self.db_path)

    def add(self, task: Task) -> Task:
        """
        Adiciona uma nova tarefa ao banco de dados.
        Retorna a tarefa com o ID preenchido.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)"
            cursor.execute(sql, (task.title, task.description, task.status))
            
            conn.commit()
            
            # Pega o ID que o banco de dados acabou de gerar
            task.id = cursor.lastrowid
            
            return task
        
        except sqlite3.Error as e:
            print(f"Erro ao adicionar tarefa: {e}")
            conn.rollback()
            return None # Ou levanta uma exceção
        
        finally:
            if conn:
                conn.close()