#CAMADA DE SERVIÇOS | logica de login e usuario
#aqui reside a inteligência do projeto. A pasta services contém toda a lógica de negócio e validações de segurança
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        #injeção de dependencia do repositório
        self.user_repository = user_repository

    #criando usuario
    def create_user(self, username, password) -> User:
        """
        Cria um novo usuário com senha criptografada.
        """
        #verifica se usuário já existe
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Nome de usuário já está em uso.")

        #hash na senha
        password_hash = generate_password_hash(password)

        new_user = User(username=username, password_hash=password_hash)
        return self.user_repository.add(new_user)

    #verificacao de login
    def authenticate(self, username, password) -> User | None:
        """
        Verifica as credenciais. Retorna o usuário se forem válidas, ou None.
        """
        user = self.user_repository.get_by_username(username)
        
        #valida senha (compara o texto puro com o hash do banco)
        if user and check_password_hash(user.password_hash, password):
            return user
        
        return None

    def get_user_by_id(self, user_id) -> User | None:
        """
        Método auxiliar necessário para o Flask-Login manter a sessão ativa.
        """
        return self.user_repository.get_by_id(user_id)
    
    #deletar usuario
    def delete_user(self, user_id: int) -> bool:
        """
        Exclui o usuário do banco de dados.
        Graças ao 'ON DELETE CASCADE' no banco, as tarefas somem automaticamente.
        """
        return self.user_repository.delete(user_id)