from flask import render_template, request, jsonify
from flask_login import login_required, current_user # [Novo] Import necessário
from services.task_service import TaskService

class HomeController:
    def __init__(self, app, task_service: TaskService):
        self.app = app
        self.task_service = task_service
        self.register_routes()

    def register_routes(self):
        
        # ROTA DA PÁGINA PRINCIPAL (Agora Protegida)
        @self.app.route('/')
        @login_required # <--- O CADEADO: Bloqueia quem não está logado
        def index():
            # O Flask-Login injeta o 'current_user' no template automaticamente,
            # mas a proteção acontece aqui. Se não estiver logado, 
            # o Flask redireciona para '/login' (configurado no app.py)
            return render_template('index.html')

        # ENDPOINT CREATE
        @self.app.route('/api/tasks', methods=['POST'])
        @login_required # Protegendo a API
        def create_task():
            try:
                data = request.get_json()
                title = data.get('title')
                description = data.get('description')
                
                new_task = self.task_service.create_task(title, description)
                
                if new_task:
                    return jsonify(new_task.to_dict()), 201
                else:
                    return jsonify({"error": "Falha ao criar tarefa"}), 500
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                print(f"Erro inesperado: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500
        
        # ENDPOINT READ
        @self.app.route('/api/tasks', methods=['GET'])
        @login_required # Protegendo a API
        def get_tasks():
            try:
                all_tasks = self.task_service.get_all_tasks()
                tasks_as_dict = [task.to_dict() for task in all_tasks]
                return jsonify(tasks_as_dict), 200
            except Exception as e:
                print(f"Erro ao buscar tarefas: {e}")
                return jsonify({"error": "Erro interno ao buscar tarefas"}), 500
    
        # ENDPOINT UPDATE
        @self.app.route('/api/tasks/<int:task_id>', methods=['PUT'])
        @login_required # Protegendo a API
        def update_task(task_id):
            try:
                data = request.get_json()
                new_status = data.get('status')

                if not new_status:
                    return jsonify({"error": "O 'status' é obrigatório"}), 400

                updated_task = self.task_service.update_task_status(task_id, new_status)
                return jsonify(updated_task.to_dict()), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 404
            except Exception as e:
                print(f"Erro inesperado ao atualizar: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500
        
        # ENDPOINT DELETE
        @self.app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
        @login_required # Protegendo a API
        def delete_task(task_id):
            try:
                success = self.task_service.delete_task(task_id)
                if success:
                    return jsonify({"success": True, "message": "Tarefa excluída"}), 200
                else:
                    return jsonify({"error": "Falha ao excluir tarefa"}), 500
            except ValueError as e:
                return jsonify({"error": str(e)}), 404
            except Exception as e:
                print(f"Erro inesperado ao excluir: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500