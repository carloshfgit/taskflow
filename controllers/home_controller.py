from flask import render_template, request, jsonify
from services.task_service import TaskService

class HomeController:
    def __init__(self, app, task_service: TaskService):
        # Recebe o app Flask e o serviço por Injeção de Dependência
        self.app = app
        self.task_service = task_service
        
        # Registra as rotas
        self.register_routes()

    def register_routes(self):
        
        # Rota para servir a página principal (o seu index.html)
        @self.app.route('/')
        def index():
            # 'index.html' deve estar dentro da pasta 'views'
            return render_template('index.html')

        # --- ENDPOINT DA API PARA O 'CREATE' ---
        @self.app.route('/api/tasks', methods=['POST'])
        def create_task():
            try:
                # 1. Pega os dados JSON enviados pelo frontend
                data = request.get_json()
                title = data.get('title')
                description = data.get('description')
                
                # 2. Chama o SERVIÇO para criar a tarefa
                new_task = self.task_service.create_task(title, description)
                
                if new_task:
                    # 3. Retorna a tarefa criada (com ID) como JSON
                    # O status 201 significa "Recurso Criado"
                    return jsonify(new_task.to_dict()), 201
                else:
                    return jsonify({"error": "Falha ao criar tarefa"}), 500
            
            except ValueError as e:
                # Erro de validação do serviço (ex: título em branco)
                return jsonify({"error": str(e)}), 400 # 400 = Bad Request
            
            except Exception as e:
                print(f"Erro inesperado: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500
        
        # --- NOVA ROTA PARA O 'READ' ---
        @self.app.route('/api/tasks', methods=['GET'])
        def get_tasks():
            try:
                # 1. Chama o serviço para buscar as tarefas
                all_tasks = self.task_service.get_all_tasks() # Retorna list[Task]
                
                # 2. Converte a lista de objetos Task em uma lista de dicionários
                tasks_as_dict = [task.to_dict() for task in all_tasks]
                
                # 3. Retorna o JSON para o frontend
                return jsonify(tasks_as_dict), 200 # 200 = OK
            
            except Exception as e:
                print(f"Erro ao buscar tarefas: {e}")
                return jsonify({"error": "Erro interno ao buscar tarefas"}), 500
    
        @self.app.route('/api/tasks/<int:task_id>', methods=['PUT'])
        def update_task(task_id):
            try:
                data = request.get_json()
                new_status = data.get('status') # Pega o status do JSON

                if not new_status:
                    return jsonify({"error": "O 'status' é obrigatório"}), 400

                # 1. Chama o serviço para fazer a atualização
                updated_task = self.task_service.update_task_status(task_id, new_status)
                
                # 2. Retorna a tarefa (com status novo ou antigo,
                #    dependendo da regra de negócio)
                return jsonify(updated_task.to_dict()), 200
            
            except ValueError as e: # Caso o serviço levante "Não encontrado"
                return jsonify({"error": str(e)}), 404 # 404 = Not Found
            
            except Exception as e:
                print(f"Erro inesperado ao atualizar: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500
        
        # --- NOVA ROTA PARA O 'DELETE' ---
        @self.app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
        def delete_task(task_id):
            try:
                # 1. Chama o serviço para excluir
                success = self.task_service.delete_task(task_id)
                
                if success:
                    # 2. Retorna uma mensagem de sucesso
                    return jsonify({"success": True, "message": "Tarefa excluída"}), 200
                else:
                    # Isso não deve acontecer se a verificação do serviço funcionar
                    return jsonify({"error": "Falha ao excluir tarefa"}), 500
            
            except ValueError as e: # Caso o serviço levante "Não encontrado"
                return jsonify({"error": str(e)}), 404 # 404 = Not Found
            
            # except PermissionError as e: # Se você implementar regras de permissão
            #     return jsonify({"error": str(e)}), 403 # 403 = Forbidden
            
            except Exception as e:
                print(f"Erro inesperado ao excluir: {e}")
                return jsonify({"error": "Erro interno do servidor"}), 500