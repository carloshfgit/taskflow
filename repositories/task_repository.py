#CAMADA DE REPOSITORIOS
#lida com toda a lógica de persistência (comandos SQL)
import sqlite3
from models.task import Task
from .base_repository import BaseRepository

class TaskRepository(BaseRepository):
    def __init__(self, db_path="taskflow.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        
        #isso faz com que o sqlite retorne as linhas como "dicionários"
        conn.row_factory = sqlite3.Row 
        
        return conn

    #CRIAR TAREFA (CREATE)
    def add(self, task: Task) -> Task:
        """
        adiciona uma nova tarefa ao banco de dados
        retorna a tarefa com o ID preenchido
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

    #BUSCAR TAREFAS (READ)
    def get_all(self) -> list[Task]:
        """
        busca todas as tarefas do banco de dados
        """
        tasks = []
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT id, title, description, status FROM tasks ORDER BY id"
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            
            #converte cada linha do banco em um objeto Task
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
            return [] #retorna lista vazia em caso de erro
        
        finally:
            if conn:
                conn.close()
        
    #BUSCAR POR ID (vou explorar melhor mais tarde)
    def get_by_id(self, task_id: int) -> Task | None:
        """
        busca uma única tarefa pelo seu ID
        retorna um objeto Task ou None se não for encontrada
        """
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
                    status=row['status']
                )
            return None #não encontrou
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar tarefa por ID: {e}")
            return None
        
        finally:
            if conn:
                conn.close()

    #ATUALIZAR TAREFA (UPDATE)
    def update(self, task: Task) -> None:
        """
        Atualiza uma tarefa existente no banco de dados.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            #atualiza todos os campos baseando-se no ID
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
            if conn:
                conn.close()

    #EXCLUIR TAREFAS (DELETE)
    def delete(self, task_id: int) -> bool:
        """
        exclui uma tarefa do banco de dados pelo seu ID
        retorna true se a exclusão foi bem-sucedida, false caso contrário
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "DELETE FROM tasks WHERE id = ?"
            cursor.execute(sql, (task_id,))
            
            conn.commit()
            
            #verifica se alguma linha foi realmente afetada (excluída)
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Erro ao excluir tarefa: {e}")
            conn.rollback()
            return False
        
        finally:
            if conn:
                conn.close()