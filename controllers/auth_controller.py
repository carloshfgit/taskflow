# CAMADA CONTROLLERS | rotas para login, cadastro, logout e exclusão de conta
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
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
                
                # chama o serviço verificador de senha
                user = self.user_service.authenticate(username, password)
                
                if user:
                    # SUCESSO: cria a sessão do usuário
                    login_user(user)
                    return redirect(url_for('index')) # Redireciona para a home
                else:
                    # FALHA: mostra mensagem de erro
                    flash('Usuário ou senha inválidos.', 'error')
            
            return render_template('login.html')

        # ROTA DE CADASTRO
        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                try:
                    # chama o serviço para criar (já com hash)
                    self.user_service.create_user(username, password)
                    flash('Conta criada com sucesso! Faça login.', 'success')
                    return redirect(url_for('login'))
                
                except ValueError as e:
                    flash(str(e), 'error')

            return render_template('register.html')

        # [NOVA ROTA] Perfil e Edição de Usuário
        @self.app.route('/profile', methods=['GET', 'POST'])
        @login_required
        def profile():
            if request.method == 'POST':
                # Coletamos os dados do input
                current_password = request.form.get('current_password')
                new_username = request.form.get('new_username')
                new_password = request.form.get('new_password')
                
                try:
                    # Chamamos o método seguro que criamos na Etapa 1
                    self.user_service.update_user_credentials(
                        user_id=current_user.id,
                        current_password=current_password,
                        new_username=new_username,
                        new_password=new_password
                    )
                    
                    flash('Perfil atualizado com sucesso!', 'success')
                    # Recarregamos a página para mostrar os dados novos
                    return redirect(url_for('profile'))
                
                except ValueError as e:
                    # Erros de negócio: Senha errada ou usuário já existente
                    flash(str(e), 'error')

            # Renderiza a view (que faremos na Etapa 3)
            # O current_user já está disponível no template automaticamente pelo Flask-Login,
            # mas podemos passar explicitamente se preferir.
            return render_template('profile.html', user=current_user)

        # ROTA DE LOGOUT
        @self.app.route('/logout')
        @login_required # só quem está logado pode deslogar
        def logout():
            logout_user() # destrói a sessão
            return redirect(url_for('login'))
        
        # ROTA PARA EXCLUIR CONTA
        @self.app.route('/delete_account', methods=['POST']) 
        @login_required
        def delete_account():
            try:
                # pega o ID do usuário logado
                user_id = current_user.id
                
                # chama o serviço para deletar
                self.user_service.delete_user(user_id)
                
                # faz logout forçado (limpa a sessão)
                logout_user()
                
                flash('Sua conta e tarefas foram excluídas.', 'success')
                return redirect(url_for('register')) # redireciona para cadastro
                
            except Exception as e:
                print(f"Erro ao excluir conta: {e}")
                flash('Erro ao excluir conta.', 'error')
                return redirect(url_for('index'))