#um script utilitário para criar o banco de dados e as tabelas iniciais.
import sqlite3

#define o nome do arquivo do banco de dados
DB_NAME = "taskflow.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

#habilita suporte a chaves estrangeiras (Foreign Keys)
#isso garante que não seja possível criar uma tarefa para um usuário que não existe
cursor.execute("PRAGMA foreign_keys = ON;")

#cria a tabela 'users' (se ainda não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
""")

#recria a tabela 'tasks' com o vínculo de usuário
cursor.execute("DROP TABLE IF EXISTS tasks;")

cursor.execute("""
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE 
);
""")

#confirma as mudanças e fecha a conexão
conn.commit()
conn.close()

print(f"Banco de dados '{DB_NAME}' atualizado com sucesso!")
print("Tabela 'tasks' recriada com coluna 'user_id'.")