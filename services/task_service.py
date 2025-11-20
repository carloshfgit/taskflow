#CAMADA DE SERVIÇOS
#contém toda a lógica e regras de negócio da aplicação

from models.task import Task
from repositories.task_repository import TaskRepository #importa a implementação

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        #recebe o repositório por injecao de dependencia
        self.task_repository = task_repository

    #CRIAR TAREFAS (CREATE)
    def create_task(self, title: str, description: str) -> Task:
        """
        cria uma nova tarefa
        aplica as regras de negócio
        """
        
        #REGRAS
        #1. validacao
        if not title:
            raise ValueError("O título é obrigatório")
            
        #2. logica de padrao
        #toda nova tarefa criada deve começar como 'todo (to do) (a fazer)'
        default_status = "todo"
    
        #cria o objeto modelo
        new_task = Task(title=title, description=description, status=default_status)
        
        #pede ao repositório para salvar
        created_task = self.task_repository.add(new_task)
        
        return created_task
    
    #BUSCAR TAREFAS (READ)
    def get_all_tasks(self) -> list[Task]:
        """
        busca todas as tarefas
        """
        #repassamos a chamada para o repositório
        return self.task_repository.get_all()
    
    #ATUALIZAR TAREFAS (UPDATE)
    def update_task_status(self, task_id: int, new_status: str) -> Task:
        """
        atualiza o status de uma tarefa, aplicando regras de negócio
        """
        #busca a tarefa
        task_to_update = self.task_repository.get_by_id(task_id)
        
        if not task_to_update:
            raise ValueError(f"Tarefa com ID {task_id} não encontrada.")
            
        #REGRAS
        #não permitir mover de 'To Do' direto para 'Done'
        is_invalid_move = task_to_update.status == "todo" and new_status == "done"
        if is_invalid_move:
            #mantém o status antigo e não salva
            print("Regra de negócio: Movimento inválido (todo -> done)")
            return task_to_update #retorna o objeto sem alteração
        
        #tualiza o objeto
        task_to_update.status = new_status
        
        #salva no repositório
        self.task_repository.update(task_to_update)
        
        return task_to_update
    
    #EXCLUIR TAREFAS (DELETE)
    def delete_task(self, task_id: int) -> bool:
        """
        exclui uma tarefa
        aplica regras de negócio
        """
        
        #mais tarde implementarei permissões de usuário aqui
        
        #verificar se a tarefa existe antes de tentar deletar
        task_to_delete = self.task_repository.get_by_id(task_id)
        if not task_to_delete:
            raise ValueError(f"Tarefa com ID {task_id} não encontrada.")
            
        #chama o repositório para excluir
        return self.task_repository.delete(task_id)