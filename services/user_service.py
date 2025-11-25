from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        # Injeção de Dependência do repositório
        self.user_repository = user_repository

    def create_user(self, username, password) -> User:
        """
        Cria um novo usuário com senha criptografada.
        """
        # REGRA 1: Verificar se usuário já existe
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Nome de usuário já está em uso.")

        # REGRA 2: Criptografar a senha (Hash)
        # O método 'pbkdf2:sha256' é o padrão seguro atual do Werkzeug
        password_hash = generate_password_hash(password)

        # Cria o objeto e manda o repositório salvar
        new_user = User(username=username, password_hash=password_hash)
        return self.user_repository.add(new_user)

    def authenticate(self, username, password) -> User | None:
        """
        Verifica as credenciais. Retorna o usuário se forem válidas, ou None.
        """
        user = self.user_repository.get_by_username(username)
        
        # REGRA 3: Validar senha (compara o texto puro com o hash do banco)
        if user and check_password_hash(user.password_hash, password):
            return user
        
        return None

    def get_user_by_id(self, user_id) -> User | None:
        """
        Método auxiliar necessário para o Flask-Login manter a sessão ativa.
        """
        return self.user_repository.get_by_id(user_id)
    
    def delete_user(self, user_id: int) -> bool:
        """
        Exclui o usuário do banco de dados.
        Graças ao 'ON DELETE CASCADE' no banco, as tarefas somem automaticamente.
        """
        return self.user_repository.delete(user_id)