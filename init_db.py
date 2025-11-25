import sqlite3

# Define o nome do arquivo do banco de dados
DB_NAME = "taskflow.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 1. Habilita suporte a chaves estrangeiras (Foreign Keys)
# Isso garante que não seja possível criar uma tarefa para um usuário que não existe
cursor.execute("PRAGMA foreign_keys = ON;")

# 2. Cria a tabela 'users' (se ainda não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
""")

# 3. Recria a tabela 'tasks' com o vínculo de usuário
# ATENÇÃO: DROP TABLE apaga todas as tarefas antigas para recriar a estrutura correta!
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

# Confirma as mudanças e fecha a conexão
conn.commit()
conn.close()

print(f"Banco de dados '{DB_NAME}' atualizado com sucesso!")
print("Tabela 'tasks' recriada com coluna 'user_id'.")