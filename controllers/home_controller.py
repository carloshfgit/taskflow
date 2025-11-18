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