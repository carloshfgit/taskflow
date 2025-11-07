from flask import render_template

class HomeController:
    def index(self):
        
        # O Controller decide qual view retornar.
        return render_template('index.html')