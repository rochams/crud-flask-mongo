from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from ..dbase.database import mongo
import re 
from bson.objectid import ObjectId

product = Blueprint('product', __name__)


@product.route('/list')
def product_list():
    if "username" in session:
        products = mongo.db.products.find()
        return render_template('produtos/listar.html', products=products)
    else:
        return redirect(url_for('users.index'))

@product.route('/insert', methods=['GET', 'POST'])
def insert_product():
    if request.method == 'GET':
        return render_template('produtos/inserir.html')
    else:
        nome = request.form.get("nome")
        quantidade = request.form.get("quantidade")
        preco = request.form.get("preco")
        categoria = request.form.get("categoria")
        estoque = request.form.get("estoque")

        if not nome or len(nome) > 100:
            flash("Digite entre 1 e 20 caracteres.")
        elif not quantidade or float(quantidade) <= 0:
            flash("Quantidade inválida.")
        elif not preco or float(preco) < 0:
            flash("Preço inválido!")
        elif not categoria:
            flash("Selecione a categoria.")
        elif not estoque:
            flash("Selecione o estoque.")
        else:
            mongo.db.products.insert_one({

                    "produto": nome,
                    "quantidade": quantidade,
                    "preco": preco,
                    "categoria": categoria,
                    "estoque": estoque,
                    "valor_total": (float(quantidade) * float(preco))               
                })
            flash("Produto cadastrado!")
        return redirect(url_for('product.product_list'))

@product.route('/edit', methods=['POST', 'GET'])
def edit_product():
    if request.method == 'GET':
        product_id = request.values.get("productId")                            # request filtra sempre pelo name, productId no caso.
        if not product_id:
            flash("[id] do produto não encontrado.")
            return redirect(url_for("product.product_list"))
        else:
            prod_id = mongo.db.products.find({'_id': ObjectId(product_id)})     # Verificando se valores correspondem. ObjectId está convertendo para o mesmo tipo do que está no Mongo.
            prods = [p for p in prod_id]
            estoque = set()
            products = mongo.db.products.find()
            for p in products:
                estoque.add(p['estoque'])
            return render_template('produtos/editar.html', prods=prods,  estoque=estoque)

    else:
        product_id = request.form.get("productId")
        nome = request.form.get("nome")
        quantidade = request.form.get("quantidade")
        preco = request.form.get("preco")
        categoria = request.form.get("categoria")
        estoque = request.form.get("estoque")

        if not product_id:
            flash("Campo [id] obrigatório.")
        elif not nome or len(nome) > 100:
            flash("Digite entre 1 e 20 caracteres.")
        elif not quantidade or float(quantidade) <= 0:
            flash("Quantidade inválida.")
        elif not preco or float(preco) < 0:
            flash("Preço inválido!")
        elif not categoria:
            flash("Selecione a categoria.")
        elif not estoque:
            flash("Selecione o estoque.")
        else:
            mongo.db.products.update({"_id": ObjectId(product_id)},
            {
                "$set":{
                    "produto": nome,
                    "quantidade": quantidade,
                    "preco": preco,
                    "categoria": categoria,
                    "estoque": estoque,
                    "valor_total": (float(quantidade) * float(preco))
                }
            })
            flash("Produto alterado com sucesso!")
        return redirect(url_for("product.product_list"))

@product.route('/delete')
def del_product():
    product_id = request.values.get("productId")
    if not product_id:
        flash("Campo [id] não encontrado.")
        return redirect(url_for("product.del_product"))
    else:
        mongo.db.products.delete_one({'_id': ObjectId(product_id)})
        flash("Produto removido com sucesso!")
        return redirect(url_for('product.product_list'))




