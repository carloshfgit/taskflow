from flask import Flask
from flask_login import LoginManager # [Novo] Import do Flask-Login

# Imports das Tarefas (Existentes)
from controllers.home_controller import HomeController
from services.task_service import TaskService
from repositories.task_repository import TaskRepository

# [Novo] Imports de Autenticação
from controllers.auth_controller import AuthController
from services.user_service import UserService
from repositories.user_repository import UserRepository

# CONFIGURAÇÃO
DB_PATH = "taskflow.db"

# Cria a aplicação Flask
app = Flask(__name__, template_folder='views', static_folder='static')

# [IMPORTANTE] Chave secreta para assinar os cookies de sessão
# Sem isso, o login não funciona. Em produção, use uma string aleatória e complexa.
app.secret_key = 'chave_muito_secreta_e_segura_do_taskflow'

# [Novo] Configuração do Gerenciador de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Define qual é a rota da página de login (função 'login')

# INJEÇÃO DE DEPENDÊNCIAS (SOLID)
# 1. Criar Repositórios (Acesso a Dados)
task_repo = TaskRepository(db_path=DB_PATH)
user_repo = UserRepository(db_path=DB_PATH) # [Novo]

# 2. Criar Serviços (Regras de Negócio)
task_service = TaskService(task_repository=task_repo)
user_service = UserService(user_repository=user_repo) # [Novo] Injeta o repo de usuários

# 3. Criar Controladores (Rotas)
# O AuthController registra as rotas /login e /register automaticamente no __init__
auth_controller = AuthController(app, user_service) 
home_controller = HomeController(app, task_service)

# [Novo] User Loader
# O Flask-Login usa essa função para buscar o objeto usuário no banco a cada request,
# baseado no ID salvo no cookie da sessão.
@login_manager.user_loader
def load_user(user_id):
    return user_service.get_user_by_id(user_id)

# EXECUÇÃO
if __name__ == "__main__":
    import os
    # Verifica se o banco existe
    if not os.path.exists(DB_PATH):
        print(f"Atenção: Banco de dados '{DB_PATH}' não encontrado.")
        print("Execute 'python init_db.py' primeiro.")
    else:
        app.run(debug=True, port=5000)