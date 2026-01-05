from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Secret key para sessões e flash (necessário para deletar produtos e mensagens)
app.secret_key = "kawa"  # você pode trocar por algo mais seguro

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configurações do banco
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "confeitaria.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Pasta para uploads
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/img/produtos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# Importa views e models
from app import view, models

# Cria tabelas se não existirem
with app.app_context():
    db.create_all()
