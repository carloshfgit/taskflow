from models.task import Task
from repositories.task_repository import TaskRepository # Importa a implementação

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        # Recebe o repositório por Injeção de Dependência
        self.task_repository = task_repository

    def create_task(self, title: str, description: str) -> Task:
        """
        Cria uma nova tarefa.
        Aplica as regras de negócio.
        """
        
        # --- REGRA DE NEGÓCIO ---
        # 1. Validação (exemplo)
        if not title:
            raise ValueError("O título é obrigatório")
            
        # 2. Lógica de Padrão
        # Toda nova tarefa criada deve começar como 'todo'
        default_status = "todo"
        # -------------------------
        
        # Cria o objeto modelo
        new_task = Task(title=title, description=description, status=default_status)
        
        # Pede ao repositório para salvar
        created_task = self.task_repository.add(new_task)
        
        return created_task
    
    # --- NOVO MÉTODO ---
    def get_all_tasks(self) -> list[Task]:
        """
        Busca todas as tarefas.
        """
        # Para o "Read All", geralmente não há regras de negócio complexas
        # Apenas repassamos a chamada para o repositório
        return self.task_repository.get_all()