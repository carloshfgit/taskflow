from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, password_hash, id=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    #método útil para quando quisermos converter o usuário para JSON (API)
    #nunca retornamos a senha/hash aqui por segurança
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }