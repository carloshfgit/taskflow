import sqlite3
from models.user import User
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db_path="taskflow.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row 
        return conn

    # [C]REATE
    def add(self, user: User) -> User:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            cursor.execute(sql, (user.username, user.password_hash))
            
            conn.commit()
            user.id = cursor.lastrowid
            return user
        except sqlite3.Error as e:
            print(f"Erro ao criar usuário: {e}")
            return None
        finally:
            if conn: conn.close()

    # [R]EAD - Buscar por ID (Usado pelo Flask-Login para manter a sessão)
    def get_by_id(self, user_id: int) -> User | None:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM users WHERE id = ?"
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            
            if row:
                return User(id=row['id'], username=row['username'], password_hash=row['password_hash'])
            return None
        except sqlite3.Error as e:
            print(f"Erro ao buscar usuário por ID: {e}")
            return None
        finally:
            if conn: conn.close()

    # [R]EAD - Buscar por Username (Essencial para o Login)
    def get_by_username(self, username: str) -> User | None:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM users WHERE username = ?"
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            
            if row:
                return User(id=row['id'], username=row['username'], password_hash=row['password_hash'])
            return None
        except sqlite3.Error as e:
            print(f"Erro ao buscar usuário por username: {e}")
            return None
        finally:
            if conn: conn.close()

    # [R]EAD - Listar todos
    def get_all(self, **filters) -> list[User]:
        users = []
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            for row in rows:
                users.append(User(id=row['id'], username=row['username'], password_hash=row['password_hash']))
            return users
        except sqlite3.Error as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            if conn: conn.close()

    # [U]PDATE - Atualizar senha ou nome (Exemplo genérico)
    def update(self, user: User) -> None:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "UPDATE users SET username = ?, password_hash = ? WHERE id = ?"
            cursor.execute(sql, (user.username, user.password_hash, user.id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao atualizar usuário: {e}")
            conn.rollback()
        finally:
            if conn: conn.close()

    # [D]ELETE
    def delete(self, user_id: int) -> bool:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = "DELETE FROM users WHERE id = ?"
            cursor.execute(sql, (user_id,))
            conn.commit()
            
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao deletar usuário: {e}")
            return False
        finally:
            if conn: conn.close()