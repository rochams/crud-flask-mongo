from flask import Blueprint
from ..dbase.database import mongo
import json, click, pandas

produto = Blueprint('produto', __name__)

@produto.cli.command('importar')
@click.argument('arquivo_csv')
def importa_csv(arquivo_csv):
    bd = mongo.db.products
    dados = pandas.read_csv(arquivo_csv)
    conv_json = json.loads(dados.to_json(orient='records'))
    bd.insert(conv_json)

    return bd.count

