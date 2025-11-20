from flask import Flask
from controllers.home_controller import HomeController
from services.task_service import TaskService
from repositories.task_repository import TaskRepository

#CONFIGURAÇÃO
DB_PATH = "taskflow.db"

#cria a aplicação Flask
app = Flask(__name__, template_folder='views', static_folder='static')


#INJEÇÃO DE DEPENDENCIAS (SOLID)
#cria as instâncias de baixo para cima (Repo -> Service -> Controller)
task_repo = TaskRepository(db_path=DB_PATH)
task_service = TaskService(task_repository=task_repo)

#injeta o 'app' e o 'service' no controlador.
#o próprio controlador registrará suas rotas no 'app'.
home_controller = HomeController(app, task_service)


#EXECUÇÃO
if __name__ == "__main__":
    #garante que o script init_db.py foi executado
    import os
    if not os.path.exists(DB_PATH):
        print(f"Atenção: Banco de dados '{DB_PATH}' não encontrado.")
        print("Execute 'python init_db.py' primeiro.")
    else:
        app.run(debug=True, port=5000)