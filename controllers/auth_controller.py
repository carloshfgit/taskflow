from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from services.user_service import UserService

class AuthController:
    def __init__(self, app, user_service: UserService):
        self.app = app
        self.user_service = user_service
        self.register_routes()

    def register_routes(self):
        
        # ROTA DE LOGIN
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                # Chama o serviço para verificar senha
                user = self.user_service.authenticate(username, password)
                
                if user:
                    # SUCESSO: Cria a sessão do usuário
                    login_user(user)
                    return redirect(url_for('index')) # Redireciona para a home
                else:
                    # FALHA: Mostra mensagem de erro
                    flash('Usuário ou senha inválidos.', 'error')
            
            return render_template('login.html')

        # ROTA DE REGISTRO (CADASTRO)
        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                try:
                    # Chama o serviço para criar (já com hash)
                    self.user_service.create_user(username, password)
                    flash('Conta criada com sucesso! Faça login.', 'success')
                    return redirect(url_for('login'))
                
                except ValueError as e:
                    # Erro de regra de negócio (ex: usuário já existe)
                    flash(str(e), 'error')

            return render_template('register.html')

        # ROTA DE LOGOUT
        @self.app.route('/logout')
        @login_required # Só quem está logado pode deslogar
        def logout():
            logout_user() # Destrói a sessão
            return redirect(url_for('login'))