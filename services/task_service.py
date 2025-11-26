#CAMADA DE SERVIÇOS | logica das tarefas
#aqui reside a inteligência do projeto. A pasta Services contém toda a lógica de negócio e validações de segurança
from models.task import Task
from repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    # [CREATE] cria tarefas ja com o usuario definido
    def create_task(self, title: str, description: str, user_id: int) -> Task:
        if not title:
            raise ValueError("O título é obrigatório")
            
        default_status = "todo"
    
        #cria o objeto já com o dono definido
        new_task = Task(
            title=title, 
            description=description, 
            status=default_status, 
            user_id=user_id
        )
        
        return self.task_repository.add(new_task)
    
    # [READ] le as tarefas do usuario atual
    def get_all_tasks(self, user_id: int) -> list[Task]:
        return self.task_repository.get_all(user_id=user_id)
    
    # [UPDATE] atualiza o status da tarefa do usuario
    def update_task_status(self, task_id: int, new_status: str, user_id: int) -> Task:
        task_to_update = self.task_repository.get_by_id(task_id)
        
        if not task_to_update:
            raise ValueError(f"Tarefa não encontrada.")
            
        #verifica se a tarefa pertence ao usuário
        if task_to_update.user_id != user_id:
            raise ValueError("Acesso negado: Você não é o dono desta tarefa.")

        if task_to_update.status == "todo" and new_status == "done":
            print("Regra de negócio: Movimento inválido")
            return task_to_update
        
        task_to_update.status = new_status
        self.task_repository.update(task_to_update)
        
        return task_to_update
    
    # [DELETE] deleta tarefa do usuario
    def delete_task(self, task_id: int, user_id: int) -> bool:
        task_to_delete = self.task_repository.get_by_id(task_id)
        
        if not task_to_delete:
            raise ValueError(f"Tarefa não encontrada.")
            
        #segurança para validar usuario
        if task_to_delete.user_id != user_id:
            raise ValueError("Acesso negado: Você não é o dono desta tarefa.")
            
        return self.task_repository.delete(task_id)