import os
from werkzeug.utils import secure_filename
from app import app, db
from flask import render_template, request, redirect, url_for
from app.models import Produto

@app.route("/")
def homepage():
    produtos = Produto.query.all()
    return render_template("index.html", produtos=produtos)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        arquivo = request.files.get("imagem")
        nome_arquivo = None
        if arquivo and arquivo.filename != "":
            nome_arquivo = secure_filename(arquivo.filename)
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo))

        produto = Produto(
            nome=request.form["nome"],
            valor=float(request.form["valor"]),
            tipo_sabor=request.form["tipo_sabor"],
            sabor_unico=request.form.get("sabor_unico"),
            sabores=request.form.get("sabores"),
            descricao=request.form["descricao"],
            frase_botao=request.form["frase_botao"],
            imagem=nome_arquivo
        )

        db.session.add(produto)
        db.session.commit()
        return redirect(url_for("homepage"))

    return render_template("admin.html")
