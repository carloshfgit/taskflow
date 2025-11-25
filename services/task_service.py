# CAMADA DE SERVIÇOS
from models.task import Task
from repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    # [CREATE] Recebe o user_id
    def create_task(self, title: str, description: str, user_id: int) -> Task:
        if not title:
            raise ValueError("O título é obrigatório")
            
        default_status = "todo"
    
        # Cria o objeto já com o dono definido
        new_task = Task(
            title=title, 
            description=description, 
            status=default_status, 
            user_id=user_id
        )
        
        return self.task_repository.add(new_task)
    
    # [READ] Recebe user_id para filtrar
    def get_all_tasks(self, user_id: int) -> list[Task]:
        return self.task_repository.get_all(user_id=user_id)
    
    # [UPDATE] Verifica propriedade
    def update_task_status(self, task_id: int, new_status: str, user_id: int) -> Task:
        task_to_update = self.task_repository.get_by_id(task_id)
        
        if not task_to_update:
            raise ValueError(f"Tarefa não encontrada.")
            
        # REGRA DE SEGURANÇA: Verifica se a tarefa pertence ao usuário
        if task_to_update.user_id != user_id:
            raise ValueError("Acesso negado: Você não é o dono desta tarefa.")

        # Regra de negócio antiga (todo -> done)
        if task_to_update.status == "todo" and new_status == "done":
            print("Regra de negócio: Movimento inválido")
            return task_to_update
        
        task_to_update.status = new_status
        self.task_repository.update(task_to_update)
        
        return task_to_update
    
    # [DELETE] Verifica propriedade
    def delete_task(self, task_id: int, user_id: int) -> bool:
        task_to_delete = self.task_repository.get_by_id(task_id)
        
        if not task_to_delete:
            raise ValueError(f"Tarefa não encontrada.")
            
        # REGRA DE SEGURANÇA
        if task_to_delete.user_id != user_id:
            raise ValueError("Acesso negado: Você não é o dono desta tarefa.")
            
        return self.task_repository.delete(task_id)