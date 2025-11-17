# Em task_service.py
from models.task import Task # Importa seu modelo

class TaskService:
    def __init__(self, task_repository):
        self.task_repository = task_repository # Injeção de Dependência

    def create_task(self, title, description):
        # REGRA DE NEGÓCIO: Novas tarefas sempre começam como 'todo'
        new_task = Task(title=title, description=description, status="todo")
        
        # Chama o REPOSITÓRIO para salvar
        created_task = self.task_repository.add(new_task)
        return created_task