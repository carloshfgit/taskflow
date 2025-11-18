import sqlite3
from models.task import Task
from .base_repository import BaseRepository

class TaskRepository(BaseRepository):
    def __init__(self, db_path="taskflow.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        
        # Isso faz com que o sqlite retorne as linhas como "dicionários"
        # facilitando o acesso por nome de coluna (ex: row['title'])
        conn.row_factory = sqlite3.Row 
        
        return conn

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
            task.id = cursor.lastrowid
            return task
        
        except sqlite3.Error as e:
            print(f"Erro ao adicionar tarefa: {e}")
            conn.rollback()
            return None
        
        finally:
            if conn:
                conn.close()

    # --- NOVO MÉTODO ---
    def get_all(self) -> list[Task]:
        """
        Busca todas as tarefas do banco de dados.
        """
        tasks = []
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT id, title, description, status FROM tasks ORDER BY id"
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            
            # Converte cada linha do banco em um objeto Task
            for row in rows:
                tasks.append(
                    Task(
                        id=row['id'],
                        title=row['title'],
                        description=row['description'],
                        status=row['status']
                    )
                )
            return tasks
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar tarefas: {e}")
            return [] # Retorna lista vazia em caso de erro
        
        finally:
            if conn:
                conn.close()