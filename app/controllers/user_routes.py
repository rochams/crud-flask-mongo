from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from ..dbase.database import mongo
from werkzeug.security import check_password_hash

users = Blueprint('users', __name__)                    # url_prefix diz que todas as userss_ terão /index antes das suas respectivas endpoints. É OPCIONAL.


@users.route('/')
def index():
    return redirect(url_for('users.login'))


@users.route('/home')
def home():
    if session["username"]:
        return render_template('usuarios/main.html')
    else:
        return redirect(url_for('users.index'))       # url_for redirecionando para a página de login (função login).

@users.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        redirect(url_for('users.home'))
    if request.method == 'POST':
        username = request.form.get('usuario')
        password = request.form.get('senha')

        userFound = mongo.db.users.find_one({'name': username})         # Caso se encontre o usuário, ele será guardado na variável
        if userFound:
            userValid= userFound["name"]                                # uFound é relativo ao usuário e pFound à senha do mesmo usuário
            passValid = userFound["password"]
            if check_password_hash(passValid, password):                # Comparativo das senhas 
                session['username'] = userValid
                return redirect(url_for('users.home'))
            else:
                flash('Senha incorreta!')
                return render_template('usuarios/login.html')
        else:
            flash('Usuário não encontrado.')
            return render_template('usuarios/login.html')
    return render_template('usuarios/login.html')


@users.route('/logout')
def logout():
    session.pop("username", None)
    flash("Sessão finalizada.")
    return redirect(url_for("users.login"))


