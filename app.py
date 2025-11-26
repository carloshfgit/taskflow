from flask import Flask
from flask_login import LoginManager 
from controllers.home_controller import HomeController
from services.task_service import TaskService
from repositories.task_repository import TaskRepository
from controllers.auth_controller import AuthController
from services.user_service import UserService
from repositories.user_repository import UserRepository

#CONFIGURAÇÃO
DB_PATH = "taskflow.db"

#cria a aplicação Flask
app = Flask(__name__, template_folder='views', static_folder='static')

#chave secreta para assinar os cookies de sessão
#sem isso, o login não funciona
app.secret_key = 'chave_muito_secreta_e_segura_do_taskflow'

#configuração do gerenciador de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #define qual é a rota da página de login (função 'login')

#INJEÇÃO DE DEPENDÊNCIAS 
#criando repositorios
task_repo = TaskRepository(db_path=DB_PATH)
user_repo = UserRepository(db_path=DB_PATH) 

#criando serviços
task_service = TaskService(task_repository=task_repo)
user_service = UserService(user_repository=user_repo) 

#criando controllers
#o AuthController registra as rotas /login e /register automaticamente no __init__
auth_controller = AuthController(app, user_service) 
home_controller = HomeController(app, task_service)

#USER LOADER
#o Flask-Login usa essa função para buscar o objeto usuário no banco a cada request,
#baseado no ID salvo no cookie da sessão
@login_manager.user_loader
def load_user(user_id):
    return user_service.get_user_by_id(user_id)

#EXECUÇÃO
if __name__ == "__main__":
    import os
    #verifica se o banco existe
    if not os.path.exists(DB_PATH):
        print(f"Atenção: Banco de dados '{DB_PATH}' não encontrado.")
        print("Execute 'python init_db.py' primeiro.")
    else:
        app.run(debug=True, port=5000)