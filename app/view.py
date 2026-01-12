from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, jsonify, current_app
)
from werkzeug.utils import secure_filename
from app import db
from app.models import Produto, Usuario
import os
import re

main_bp = Blueprint('main', __name__)

# =========================
# HOME
# =========================
@main.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)

# =========================
# ACESSO AO DELIVERY
# =========================
@main_bp.route('/acesso-delivery')
def acesso_delivery():
    if 'usuario_id' not in session:
        flash("Cadastre-se para acessar o delivery", "warning")
        return redirect(url_for('main.cadastro'))
    return redirect(url_for('main.delivery'))

# =========================
# DELIVERY / CARDÁPIO
# =========================
@main_bp.route('/delivery')
def delivery():
    usuario = None
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])

    produtos = Produto.query.all()
    return render_template(
        'delivery.html',
        produtos=produtos,
        usuario=usuario
    )

# =========================
# BUSCA (AJAX)
# =========================
@main_bp.route('/buscar_produtos')
def buscar_produtos():
    termo = request.args.get('q', '').strip()
    if not termo:
        return jsonify([])

    produtos = Produto.query.filter(
        (Produto.nome.ilike(f"%{termo}%")) |
        (Produto.descricao.ilike(f"%{termo}%"))
    ).all()

    return jsonify([
        {
            "id": p.id,
            "nome": p.nome,
            "descricao": p.descricao,
            "valor_venda": float(p.valor_venda),
            "imagem": p.imagem,
            "frase_botao": p.frase_botao
        } for p in produtos
    ])

# =========================
# ADMIN
# =========================
@main_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        preco_custo = float(request.form['preco_custo'])
        valor_venda = float(request.form['valor_venda'])

        produto = Produto(
            nome=request.form['nome'],
            preco_custo=preco_custo,
            valor_venda=valor_venda,
            lucro=valor_venda - preco_custo,
            descricao=request.form['descricao'],
            tipo_sabor=request.form['tipo_sabor'],
            sabor_unico=request.form.get('sabor_unico'),
            sabores=request.form.get('sabores'),
            frase_botao=request.form['frase_botao']
        )

        imagem = request.files.get('imagem')
        if imagem and imagem.filename:
            filename = secure_filename(imagem.filename)
            caminho = os.path.join(
                current_app.config['UPLOAD_FOLDER_PRODUTOS'],
                filename
            )
            imagem.save(caminho)
            produto.imagem = filename

        db.session.add(produto)
        db.session.commit()
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for('main.admin'))

    return render_template(
        'admin.html',
        produtos=Produto.query.all(),
        usuarios=Usuario.query.all()
    )

# =========================
# CARRINHO
# =========================
@main_bp.route('/carrinho/adicionar/<int:id>', methods=['POST'])
def adicionar_carrinho(id):
    carrinho = session.get('carrinho', {})
    carrinho[str(id)] = carrinho.get(str(id), 0) + 1
    session['carrinho'] = carrinho
    session.modified = True

    flash("Produto adicionado ao carrinho!", "success")
    return redirect(url_for('main.delivery'))

@main_bp.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', {})
    itens = []
    total = 0

    for produto_id, qtd in carrinho.items():
        produto = Produto.query.get(int(produto_id))
        if produto:
            subtotal = produto.valor_venda * qtd
            total += subtotal
            itens.append({
                'produto': produto,
                'quantidade': qtd,
                'subtotal': subtotal
            })

    return render_template('carrinho.html', itens=itens, total=total)

# =========================
# LOGIN
# =========================
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(
            email=request.form['email']
        ).first()

        if usuario and usuario.check_senha(request.form['senha']):
            session['usuario_id'] = usuario.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('main.delivery'))

        flash("Email ou senha inválidos", "danger")

    return render_template('login.html')

# =========================
# LOGOUT
# =========================
@main_bp.route('/logout')
def logout():
    session.clear()
    flash("Logout realizado", "success")
    return redirect(url_for('main.home'))

# =========================
# CADASTRO
# =========================
@main_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        if Usuario.query.filter_by(email=request.form['email']).first():
            flash("Email já cadastrado", "warning")
            return redirect(url_for('main.login'))

        usuario = Usuario(
            nome=request.form['nome'],
            email=request.form['email'],
            cpf=request.form.get('cpf'),
            cep=request.form['cep'],
            rua=request.form['rua'],
            bairro=request.form.get('bairro'),
            cidade=request.form.get('cidade'),
            tipo_residencia=request.form['tipo_residencia'],
            numero=request.form['numero'],
            complemento=request.form.get('complemento'),
        )
        usuario.set_senha(request.form['senha'])

        db.session.add(usuario)
        db.session.commit()
        session['usuario_id'] = usuario.id

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('main.delivery'))

    return render_template('cadastro.html')
