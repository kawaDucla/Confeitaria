from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


app.secret_key = "kawa"  

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "confeitaria.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Pasta de produtos
UPLOAD_FOLDER_PRODUTOS = os.path.join(BASE_DIR, "static/img/produtos")
os.makedirs(UPLOAD_FOLDER_PRODUTOS, exist_ok=True)
app.config['UPLOAD_FOLDER_PRODUTOS'] = UPLOAD_FOLDER_PRODUTOS

# Pasta de usuários
UPLOAD_FOLDER_USUARIOS = os.path.join(BASE_DIR, "static/img/usuarios")
os.makedirs(UPLOAD_FOLDER_USUARIOS, exist_ok=True)
app.config['UPLOAD_FOLDER_USUARIOS'] = UPLOAD_FOLDER_USUARIOS


db = SQLAlchemy(app)


from app import view, models


with app.app_context():
    db.create_all()
