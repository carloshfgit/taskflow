from flask import render_template
from flask import request, jsonify

class HomeController:
    def index(self):
        
        # O Controller decide qual view retornar.
        return render_template('index.html')
    
# Rota para criar uma nova tarefa
@app.route('/api/tasks', methods=['POST'])
def create_task_route():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    
    # 1. Validação básica de entrada
    if not title:
        return jsonify({"error": "Title is required"}), 400
        
    try:
        # 2. Chama o SERVIÇO para criar a tarefa
        new_task = self.task_service.create_task(title, description)
        
        # 3. Retorna a tarefa criada (com ID) como JSON
        return jsonify(new_task.to_dict()), 201 # 201 = Created
    except Exception as e:
        return jsonify({"error": str(e)}), 500