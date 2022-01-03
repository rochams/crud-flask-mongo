from flask import Flask
from .controllers.user_routes import users
from .controllers.product_routes import product
from ..dbase import database
from .models.users_cmd import user_commands
from .models.produtos_cmd import produto

# Para melhorar um pouco mais e isolar os recursos da minha aplicação, criamos uma função que conterá estes recursos e até mesmo dificultar uma
# eventual tentativa de chamar a minha instância do Flask (app) e muda a abordagem anterior de deixar as configurações soltas

def create_app(config_object="app.config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(users)
    app.register_blueprint(product)
    app.register_blueprint(user_commands)
    app.register_blueprint(produto)
    database.init_app(app)

    return app      # autoexecução do app    



