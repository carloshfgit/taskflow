#CAMADA CONTROLLERS | rotas para login, cadastro, logout e exclusão de conta
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from services.user_service import UserService

class AuthController:
    def __init__(self, app, user_service: UserService):
        self.app = app
        self.user_service = user_service
        self.register_routes()

    def register_routes(self):
        
        #ROTA DE LOGIN
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                #chama o serviço veriificador de senha
                user = self.user_service.authenticate(username, password)
                
                if user:
                    # SUCESSO: cria a sessão do usuário
                    login_user(user)
                    return redirect(url_for('index')) # Redireciona para a home
                else:
                    # FALHA: mostra mensagem de erro
                    flash('Usuário ou senha inválidos.', 'error')
            
            return render_template('login.html')

        #ROTA DE CADASTRO
        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                try:
                    #chama o serviço para criar (já com hash)
                    self.user_service.create_user(username, password)
                    flash('Conta criada com sucesso! Faça login.', 'success')
                    return redirect(url_for('login'))
                
                except ValueError as e:
                    flash(str(e), 'error')

            return render_template('register.html')

        # ROTA DE LOGOUT
        @self.app.route('/logout')
        @login_required #só quem está logado pode deslogar
        def logout():
            logout_user() #destrói a sessão
            return redirect(url_for('login'))
        
        #ROTA PARA EXCLUIR CONTA
        @self.app.route('/delete_account', methods=['POST']) 
        @login_required
        def delete_account():
            try:
                #pega o ID do usuário logado
                user_id = current_user.id
                
                #chama o serviço para deletar
                self.user_service.delete_user(user_id)
                
                #faz logout forçado (limpa a sessão)
                logout_user()
                
                flash('Sua conta e tarefas foram excluídas.', 'success')
                return redirect(url_for('register')) #redireciona para cadastro
                
            except Exception as e:
                print(f"Erro ao excluir conta: {e}")
                flash('Erro ao excluir conta.', 'error')
                return redirect(url_for('index'))