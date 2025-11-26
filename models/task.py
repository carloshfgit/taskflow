# CAMADA DE MODELOS
class Task:
    #adicionamos 'user_id' nos parâmetros 
    def __init__(self, title, description, status, user_id=None, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status # "todo", "doing", "done"
        self.user_id = user_id # Novo atributo para identificar o dono

    #essencial para serializar o objeto para a API
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "user_id": self.user_id 
        }