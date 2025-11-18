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
    
    # --- NOVO MÉTODO ---
    def update_task_status(self, task_id: int, new_status: str) -> Task:
        """
        Atualiza o status de uma tarefa, aplicando regras de negócio.
        """
        # 1. Busca a tarefa
        task_to_update = self.task_repository.get_by_id(task_id)
        
        if not task_to_update:
            raise ValueError(f"Tarefa com ID {task_id} não encontrada.")
            
        # 2. ---- AQUI VIVEM AS REGRAS DE NEGÓCIO ----
        # Exemplo de regra: não permitir mover de 'To Do' direto para 'Done'
        is_invalid_move = task_to_update.status == "todo" and new_status == "done"
        if is_invalid_move:
            # Mantém o status antigo e não salva
            print("Regra de negócio: Movimento inválido (todo -> done)")
            return task_to_update # Retorna o objeto sem alteração
        # ---------------------------------------------
            
        # 3. Atualiza o objeto
        task_to_update.status = new_status
        
        # 4. Salva no repositório
        self.task_repository.update(task_to_update)
        
        return task_to_update
    
    # --- NOVO MÉTODO ---
    def delete_task(self, task_id: int) -> bool:
        """
        Exclui uma tarefa.
        Aplica regras de negócio (ex: permissões).
        """
        
        # 1. ---- AQUI VIVEM AS REGRAS DE NEGÓCIO ----
        # Exemplo: Verificar se o usuário tem permissão (requer login)
        # user_permission = self.auth_service.check_permission(user_id, task_id)
        # if not user_permission:
        #     raise PermissionError("Usuário não tem permissão para excluir esta tarefa.")
        # ---------------------------------------------
        
        # 2. (Opcional) Verificar se a tarefa existe antes de tentar deletar
        task_to_delete = self.task_repository.get_by_id(task_id)
        if not task_to_delete:
            raise ValueError(f"Tarefa com ID {task_id} não encontrada.")
            
        # 3. Chama o repositório para excluir
        return self.task_repository.delete(task_id)