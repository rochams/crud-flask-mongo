from flask import Blueprint
import click
import getpass                                          # biblioteca com funcionalidades de senha
from werkzeug.security import generate_password_hash    # biblioteca para 
from ..dbase.database import mongo

user_commands = Blueprint('user', __name__)             # user está sendo especificado como uma espécie de gênero do comando, e getUser é um dos tantos comandos que posso setar.


# Criando os comandos para usuário, diferentemente do route com a decoradora, pois agora os comandos serão via cli


@user_commands.cli.command("getUser")                   # Criando comando get_user
@click.argument("name")                                 # Usando decoradora e passando o argumento pra função através da biblioteca click
def get_user(name):
    userCollection = mongo.db.users
    user = [u for u in userCollection.find({ "name": name })]   # List comprehension para verificar se o campo "name" é igual ao name que eu passei.
    print(user)


@user_commands.cli.command("addUser")                   # Função para adicionar usuários
@click.argument("name")
def create_user(name):
    userCollection = mongo.db.users
    password = getpass.getpass()
    user = {
        "name": name,
        "password": generate_password_hash(password)    # atribuindo um hash à senha através da biblioteca
    }

    userExist = userCollection.find_one({'name': name})

    if userExist:
        print (f'Usuário "{name}" já existe.')
    else:
        userCollection.insert_one(user)
        print('Usuário cadastrado com sucesso!')


@user_commands.cli.command('delUser')                   # Dropar usuário
@click.argument("name")
def del_user(name):
    userCollection = mongo.db.users
    userExist = userCollection.find_one({'name': name})
    if userExist:
        q = input(f'Deseja realmente excluir "{name}"? [S/N]:')
        if q.lower() == 's':
            userCollection.delete_one({'name': name})
            print('Usuário excluído com sucesso!')
        else:
            exit()
    else:
        print(f'Usuário "{name}" não encontrado.')


