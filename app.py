from flask import Flask
from flask_login import LoginManager, current_user # Importamos current_user
from flask_socketio import SocketIO, join_room    # Importamos ferramentas do SocketIO
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
app.secret_key = 'chave_muito_secreta_e_segura_do_taskflow'

# [NOVO] Configuração do SocketIO
# Envolvemos o app Flask. O parâmetro cors_allowed_origins='*' ajuda em desenvolvimento
socketio = SocketIO(app, cors_allowed_origins="*")

#configuração do gerenciador de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

#INJEÇÃO DE DEPENDÊNCIAS 
#criando repositorios
task_repo = TaskRepository(db_path=DB_PATH)
user_repo = UserRepository(db_path=DB_PATH) 

#criando serviços
task_service = TaskService(task_repository=task_repo)
user_service = UserService(user_repository=user_repo) 

#criando controllers
auth_controller = AuthController(app, user_service) 
# Passamos o socketio como terceiro parâmetro
home_controller = HomeController(app, task_service, socketio)

#USER LOADER
@login_manager.user_loader
def load_user(user_id):
    return user_service.get_user_by_id(user_id)

# [NOVO] Evento de Conexão WebSocket
@socketio.on('connect')
def handle_connect():
    """
    Executado automaticamente quando o frontend conecta.
    Coloca o usuário em uma 'sala' exclusiva baseada no seu ID.
    """
    if current_user.is_authenticated:
        room_name = f"user_{current_user.id}"
        join_room(room_name)
        print(f" >> WebSocket: Usuário {current_user.username} entrou na sala {room_name}")
    else:
        print(" >> WebSocket: Conexão anônima rejeitada ou ignorada.")
        return False # Rejeita a conexão se não estiver logado

#EXECUÇÃO
if __name__ == "__main__":
    import os
    if not os.path.exists(DB_PATH):
        print(f"Atenção: Banco de dados '{DB_PATH}' não encontrado.")
        print("Execute 'python init_db.py' primeiro.")
    else:
        # [ALTERADO] Usamos socketio.run em vez de app.run
        print("Iniciando servidor com suporte a WebSocket...")
        socketio.run(app, debug=True, port=5000)