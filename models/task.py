class Task:
    def __init__(self, id: int, title: str, description: str, status: str = "A Fazer"):
        self.id = id
        self.title = title
        self.description = description
        self.status = status # Ex: "A Fazer", "Fazendo", "Concluído"

    def __repr__(self):
        return f"<Task {self.id}: {self.title} ({self.status})>"