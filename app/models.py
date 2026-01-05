# importação das bibliotecas
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user (user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)


class Livro (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    autor = db.Column (db.String, nullable = True)
    titulo = db.Column (db.String, nullable = True)
    ano_publicacao = db.Column (db.Integer, nullable = True)
    genero = db.Column (db.String, nullable = True)
    quantidade = db.Column (db.Integer, nullable = True)