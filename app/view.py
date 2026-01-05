from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Produto
import os

@app.route('/')
def homepage():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Dados do formulário
        nome = request.form['nome']
        preco_custo = float(request.form['preco_custo'])
        valor_venda = float(request.form['valor_venda'])
        lucro = valor_venda - preco_custo
        descricao = request.form['descricao']
        tipo_sabor = request.form['tipo_sabor']
        sabor_unico = request.form.get('sabor_unico')
        sabores = request.form.get('sabores')
        frase_botao = request.form['frase_botao']

        # Upload de imagem
        imagem_file = request.files.get('imagem')
        if imagem_file and imagem_file.filename != '':
            filename = secure_filename(imagem_file.filename)
            imagem_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        produto = Produto(
            nome=nome,
            preco_custo=preco_custo,
            valor_venda=valor_venda,
            lucro=lucro,
            descricao=descricao,
            tipo_sabor=tipo_sabor,
            sabor_unico=sabor_unico,
            sabores=sabores,
            frase_botao=frase_botao,
            imagem=filename
        )
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('admin'))

    produtos = Produto.query.all()
    return render_template('admin.html', produtos=produtos)

# Rota para deletar produto
@app.route('/produto/deletar/<int:id>')
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    if produto.imagem:
        # Remove imagem antiga
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], produto.imagem)
        if os.path.exists(caminho_imagem):
            os.remove(caminho_imagem)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('admin'))

# Rota para editar produto
@app.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)

    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.preco_custo = float(request.form['preco_custo'])
        produto.valor_venda = float(request.form['valor_venda'])
        produto.lucro = produto.valor_venda - produto.preco_custo
        produto.descricao = request.form['descricao']
        produto.tipo_sabor = request.form['tipo_sabor']
        produto.sabor_unico = request.form.get('sabor_unico')
        produto.sabores = request.form.get('sabores')
        produto.frase_botao = request.form['frase_botao']

        imagem_file = request.files.get('imagem')
        if imagem_file and imagem_file.filename != '':
            # Apaga imagem antiga
            if produto.imagem:
                caminho_antigo = os.path.join(app.config['UPLOAD_FOLDER'], produto.imagem)
                if os.path.exists(caminho_antigo):
                    os.remove(caminho_antigo)
            filename = secure_filename(imagem_file.filename)
            imagem_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            produto.imagem = filename

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin'))

    return render_template('editar_produto.html', produto=produto)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # Aqui você pode colocar a lógica de cadastro, por enquanto só renderiza o template
    return render_template('cadastro.html')

@app.route('/login')
def login():
    return "Tela de login - ainda não implementada"
