# CAMADA DE SERVIÇOS | logica de login e usuario
# aqui reside a inteligência do projeto. A pasta services contém toda a lógica de negócio e validações de segurança
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        # injeção de dependencia do repositório
        self.user_repository = user_repository

    # criando usuario
    def create_user(self, username, password) -> User:
        """
        Cria um novo usuário com senha criptografada.
        """
        # verifica se usuário já existe
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Nome de usuário já está em uso.")

        # hash na senha
        password_hash = generate_password_hash(password)

        new_user = User(username=username, password_hash=password_hash)
        return self.user_repository.add(new_user)

    # verificacao de login
    def authenticate(self, username, password) -> User | None:
        """
        Verifica as credenciais. Retorna o usuário se forem válidas, ou None.
        """
        user = self.user_repository.get_by_username(username)
        
        # valida senha (compara o texto puro com o hash do banco)
        if user and check_password_hash(user.password_hash, password):
            return user
        
        return None

    def get_user_by_id(self, user_id) -> User | None:
        """
        Método auxiliar necessário para o Flask-Login manter a sessão ativa.
        """
        return self.user_repository.get_by_id(user_id)
    
    # [NOVO] Atualizar credenciais do usuário
    def update_user_credentials(self, user_id: int, current_password: str, new_username: str = None, new_password: str = None) -> User:
        """
        Atualiza nome de usuário e/ou senha, mediante confirmação da senha atual.
        """
        # 1. Busca o usuário atual no banco
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        # 2. Segurança: Verifica se a senha atual informada está correta
        if not check_password_hash(user.password_hash, current_password):
            raise ValueError("A senha atual está incorreta.")

        # 3. Validação de Username (apenas se mudou)
        if new_username and new_username != user.username:
            # Verifica se o novo nome já está em uso por outra pessoa
            existing_user = self.user_repository.get_by_username(new_username)
            if existing_user:
                raise ValueError("Este nome de usuário já está em uso.")
            user.username = new_username

        # 4. Atualização de Senha (apenas se informado)
        if new_password and new_password.strip():
            user.password_hash = generate_password_hash(new_password)

        # 5. Persiste as mudanças no banco
        self.user_repository.update(user)
        
        return user

    # deletar usuario
    def delete_user(self, user_id: int) -> bool:
        """
        Exclui o usuário do banco de dados.
        Graças ao 'ON DELETE CASCADE' no banco, as tarefas somem automaticamente.
        """
        return self.user_repository.delete(user_id)