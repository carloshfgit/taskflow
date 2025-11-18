import sqlite3

# Define o nome do arquivo do banco de dados
DB_NAME = "taskflow.db"

# Conecta ao banco de dados (ele será criado se não existir)
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Cria a tabela 'tasks' se ela não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL
);
""")

# Confirma as mudanças e fecha a conexão
conn.commit()
conn.close()

print(f"Banco de dados '{DB_NAME}' e tabela 'tasks' criados com sucesso.")