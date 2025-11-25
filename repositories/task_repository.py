# CAMADA DE REPOSITORIOS
import sqlite3
from models.task import Task
from .base_repository import BaseRepository

class TaskRepository(BaseRepository):
    def __init__(self, db_path="taskflow.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row 
        return conn

    # [CREATE] Agora salva o user_id
    def add(self, task: Task) -> Task:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (task.title, task.description, task.status, task.user_id))
            
            conn.commit()
            task.id = cursor.lastrowid
            return task
        
        except sqlite3.Error as e:
            print(f"Erro ao adicionar tarefa: {e}")
            conn.rollback()
            return None
        finally:
            if conn: conn.close()

    # [READ] Agora filtra pelo user_id
    def get_all(self, **filters) -> list[Task]:

        user_id = filters.get('user_id')

        if user_id is None:
            return []

        tasks = []
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM tasks WHERE user_id = ? ORDER BY id"
            cursor.execute(sql, (user_id,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                tasks.append(
                    Task(
                        id=row['id'],
                        title=row['title'],
                        description=row['description'],
                        status=row['status'],
                        user_id=row['user_id']
                    )
                )
            return tasks
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar tarefas: {e}")
            return []
        finally:
            if conn: conn.close()
        
    # [READ ONE]
    def get_by_id(self, task_id: int) -> Task | None:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM tasks WHERE id = ?"
            cursor.execute(sql, (task_id,))
            
            row = cursor.fetchone()
            
            if row:
                return Task(
                    id=row['id'],
                    title=row['title'],
                    description=row['description'],
                    status=row['status'],
                    user_id=row['user_id']
                )
            return None
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar tarefa por ID: {e}")
            return None
        finally:
            if conn: conn.close()

    # [UPDATE]
    def update(self, task: Task) -> None:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = """
            UPDATE tasks 
            SET title = ?, description = ?, status = ?
            WHERE id = ?
            """
            cursor.execute(sql, (task.title, task.description, task.status, task.id))
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"Erro ao atualizar tarefa: {e}")
            conn.rollback()
        finally:
            if conn: conn.close()

    # [DELETE]
    def delete(self, task_id: int) -> bool:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "DELETE FROM tasks WHERE id = ?"
            cursor.execute(sql, (task_id,))
            conn.commit()
            
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Erro ao excluir tarefa: {e}")
            conn.rollback()
            return False
        finally:
            if conn: conn.close()