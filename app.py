from flask import Flask
from controllers.home_controller import HomeController
from services.task_service import TaskService
from repositories.task_repository import TaskRepository

# --- CONFIGURAÇÃO ---
DB_PATH = "taskflow.db"

# 1. Cria a aplicação Flask
# 'views' é o padrão do Flask para templates (index.html)
# 'static' é o padrão para css/js
app = Flask(__name__, template_folder='views', static_folder='static')


# --- INJEÇÃO DE DEPENDÊNCIAS (Onde o SOLID ganha vida) ---

# 2. Cria as instâncias de baixo para cima (Repo -> Service -> Controller)
task_repo = TaskRepository(db_path=DB_PATH)
task_service = TaskService(task_repository=task_repo)

# 3. Injeta o 'app' e o 'service' no controlador.
# O próprio controlador registrará suas rotas no 'app'.
home_controller = HomeController(app, task_service)


# --- EXECUÇÃO ---
if __name__ == "__main__":
    # Garante que o script init_db.py foi executado
    import os
    if not os.path.exists(DB_PATH):
        print(f"Atenção: Banco de dados '{DB_PATH}' não encontrado.")
        print("Execute 'python init_db.py' primeiro.")
    else:
        app.run(debug=True, port=5000)