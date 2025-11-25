# CAMADA DE CONTROLADORES
from flask import render_template, request, jsonify
from flask_login import login_required, current_user # Importamos o current_user
from services.task_service import TaskService

class HomeController:
    def __init__(self, app, task_service: TaskService):
        self.app = app
        self.task_service = task_service
        self.register_routes()

    def register_routes(self):
        
        # ROTA INDEX (Protegida)
        @self.app.route('/')
        @login_required 
        def index():
            # Renderiza o HTML. O current_user já está disponível no template
            return render_template('index.html')

        # [CREATE] - Adicionar Tarefa
        @self.app.route('/api/tasks', methods=['POST'])
        @login_required 
        def create_task():
            try:
                data = request.get_json()
                title = data.get('title')
                description = data.get('description')
                
                # MUDANÇA PRINCIPAL:
                # Passamos o ID do usuário logado para o serviço
                user_id = current_user.id
                
                new_task = self.task_service.create_task(title, description, user_id)
                
                if new_task:
                    return jsonify(new_task.to_dict()), 201
                else:
                    return jsonify({"error": "Falha ao criar tarefa"}), 500
            
            except ValueError as e:
                return jsonify({"error": str(e)}), 400 
            
            except Exception as e:
                print(f"Erro inesperado: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500
        
        # [READ] - Listar Tarefas
        @self.app.route('/api/tasks', methods=['GET'])
        @login_required 
        def get_tasks():
            try:
                # MUDANÇA PRINCIPAL:
                # O serviço agora pede o ID para filtrar só as tarefas desse usuário
                user_id = current_user.id
                
                all_tasks = self.task_service.get_all_tasks(user_id)
                
                tasks_as_dict = [task.to_dict() for task in all_tasks]
                return jsonify(tasks_as_dict), 200 
            
            except Exception as e:
                print(f"Erro ao buscar tarefas: {e}")
                return jsonify({"error": "Erro interno ao buscar tarefas"}), 500
    
        # [UPDATE] - Atualizar Status
        @self.app.route('/api/tasks/<int:task_id>', methods=['PUT'])
        @login_required 
        def update_task(task_id):
            try:
                data = request.get_json()
                new_status = data.get('status') 

                if not new_status:
                    return jsonify({"error": "O 'status' é obrigatório"}), 400

                # MUDANÇA PRINCIPAL:
                # Passamos o user_id para o serviço verificar se somos donos da tarefa
                user_id = current_user.id

                updated_task = self.task_service.update_task_status(task_id, new_status, user_id)
                
                return jsonify(updated_task.to_dict()), 200
            
            except ValueError as e: # Erro de validação ou Acesso Negado
                return jsonify({"error": str(e)}), 404 # Ou 403 Forbidden, mas 404 é mais seguro
            
            except Exception as e:
                print(f"Erro inesperado ao atualizar: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500
        
        # [DELETE] - Excluir Tarefa
        @self.app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
        @login_required 
        def delete_task(task_id):
            try:
                user_id = current_user.id
                
                # MUDANÇA PRINCIPAL: Verifica propriedade antes de deletar
                success = self.task_service.delete_task(task_id, user_id)
                
                if success:
                    return jsonify({"success": True, "message": "Tarefa excluída"}), 200
                else:
                    return jsonify({"error": "Falha ao excluir tarefa"}), 500
            
            except ValueError as e: 
                return jsonify({"error": str(e)}), 404 
     
            except Exception as e:
                print(f"Erro inesperado ao excluir: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500