from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from app import app, db
from app.models import Produto, Usuario
import os
import re


# HOME 
@app.route('/', methods=['GET'])
def home():
    usuario = None
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])

    return render_template('home.html', usuario=usuario)



# ACESSO AO DELIVERY

@app.route('/acesso-delivery')
def acesso_delivery():
    if 'usuario_id' not in session:
        flash("Cadastre-se para acessar o delivery", "warning")
        return redirect(url_for('cadastro'))

    return redirect(url_for('delivery'))



# DELIVERY (CARDÁPIO)

@app.route('/delivery', methods=['GET'])
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



# BUSCA DE PRODUTOS (AJAX)

@app.route('/buscar_produtos')
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



# ADMIN

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        nome = request.form['nome']
        preco_custo = float(request.form['preco_custo'])
        valor_venda = float(request.form['valor_venda'])
        lucro = valor_venda - preco_custo
        descricao = request.form['descricao']
        tipo_sabor = request.form['tipo_sabor']
        sabor_unico = request.form.get('sabor_unico')
        sabores = request.form.get('sabores')
        frase_botao = request.form['frase_botao']

        imagem_file = request.files.get('imagem')
        if imagem_file and imagem_file.filename:
            filename = secure_filename(imagem_file.filename)
            caminho = os.path.join(app.config['UPLOAD_FOLDER_PRODUTOS'], filename)
            imagem_file.save(caminho)
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
        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for('admin'))

    produtos = Produto.query.all()
    usuarios = Usuario.query.all()
    return render_template('admin.html', produtos=produtos, usuarios=usuarios)



# PRODUTO (ADMIN)

@app.route('/produto/deletar/<int:id>')
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)

    if produto.imagem:
        caminho = os.path.join(app.config['UPLOAD_FOLDER_PRODUTOS'], produto.imagem)
        if os.path.exists(caminho):
            os.remove(caminho)

    db.session.delete(produto)
    db.session.commit()
    flash("Produto deletado com sucesso!", "success")
    return redirect(url_for('admin'))


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
        if imagem_file and imagem_file.filename:
            if produto.imagem:
                caminho_antigo = os.path.join(app.config['UPLOAD_FOLDER_PRODUTOS'], produto.imagem)
                if os.path.exists(caminho_antigo):
                    os.remove(caminho_antigo)

            filename = secure_filename(imagem_file.filename)
            caminho = os.path.join(app.config['UPLOAD_FOLDER_PRODUTOS'], filename)
            imagem_file.save(caminho)
            produto.imagem = filename

        db.session.commit()
        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for('admin'))

    return render_template('editar_produto.html', produto=produto)



# CADASTRO

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpf = request.form.get('cpf', '').strip()
        cep = request.form['cep']
        rua = request.form['rua']
        bairro = request.form.get('bairro', '')
        cidade = request.form.get('cidade', '')
        tipo_residencia = request.form['tipo_residencia']
        complemento = request.form.get('complemento', '')

        if tipo_residencia == "casa":
            numero = request.form.get('numero', '')
        else:
            bloco = request.form.get('bloco', '')
            apartamento = request.form.get('apartamento', '')
            numero = f"Bloco {bloco}, Apto {apartamento}"

        if cpf and not validar_cpf(cpf):
            flash("CPF inválido!", "danger")
            return render_template('cadastro.html')

        if cpf and Usuario.query.filter_by(cpf=cpf).first():
            flash("CPF já cadastrado!", "warning")
            return render_template('cadastro.html')

        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado!", "warning")
            return redirect(url_for('login'))

        imagem_file = request.files.get('imagem')
        if imagem_file and imagem_file.filename:
            filename = secure_filename(imagem_file.filename)
            caminho = os.path.join(app.config['UPLOAD_FOLDER_USUARIOS'], filename)
            imagem_file.save(caminho)
        else:
            filename = 'usuario-verificado.png'

        usuario = Usuario(
            nome=nome,
            email=email,
            cpf=cpf,
            cep=cep,
            rua=rua,
            bairro=bairro,
            cidade=cidade,
            tipo_residencia=tipo_residencia,
            numero=numero,
            complemento=complemento,
            imagem=filename
        )
        usuario.set_senha(senha)

        db.session.add(usuario)
        db.session.commit()
        session['usuario_id'] = usuario.id

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('delivery'))

    return render_template('cadastro.html')



# LOGIN / LOGOUT

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_senha(senha):
            session['usuario_id'] = usuario.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('delivery'))

        flash("Email ou senha incorretos!", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash("Você saiu da conta com sucesso!", "success")
    return redirect(url_for('home'))



# PERFIL

@app.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        flash("Cadastre-se primeiro!", "warning")
        return redirect(url_for('cadastro'))

    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)



# USUÁRIOS (ADMIN)

@app.route('/usuario/deletar/<int:id>')
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.imagem and usuario.imagem != 'usuario-verificado.png':
        caminho = os.path.join(app.config['UPLOAD_FOLDER_USUARIOS'], usuario.imagem)
        if os.path.exists(caminho):
            os.remove(caminho)

    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário deletado com sucesso!", "success")
    return redirect(url_for('admin'))

# EDITAR USUÁRIO (ADMIN)

@app.route('/usuario/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.cpf = request.form.get('cpf', '')
        usuario.cep = request.form.get('cep', '')
        usuario.rua = request.form.get('rua', '')
        usuario.bairro = request.form.get('bairro', '')
        usuario.cidade = request.form.get('cidade', '')
        usuario.complemento = request.form.get('complemento', '')

        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for('admin'))

    return render_template('editar_usuario.html', usuario=usuario)




# VALIDA CPF

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calc_dv(parte):
        soma = sum(int(parte[i]) * (len(parte) + 1 - i) for i in range(len(parte)))
        dv = 11 - (soma % 11)
        return dv if dv < 10 else 0

    dv1 = calc_dv(cpf[:9])
    dv2 = calc_dv(cpf[:9] + str(dv1))
    return cpf[-2:] == f"{dv1}{dv2}"
