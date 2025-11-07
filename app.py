
from flask import Flask
from controllers.home_controller import HomeController

app = Flask(__name__, template_folder='views', static_folder='static')

home_controller = HomeController()

@app.route('/')
def home():
    return home_controller.index()

if __name__ == '__main__':
    app.run(debug=True)