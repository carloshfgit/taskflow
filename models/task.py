#CAMADA DE MODELOS
class Task:
    def __init__(self, title, description, status, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status # "todo", "doing", "done"

    #essencial para serializar o objeto para a API
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }