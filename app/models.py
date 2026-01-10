from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re
from sqlalchemy.orm import validates

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco_custo = db.Column(db.Float, nullable=False)
    valor_venda = db.Column(db.Float, nullable=False)
    lucro = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    tipo_sabor = db.Column(db.String(20), nullable=False)
    sabor_unico = db.Column(db.String(50), nullable=True)
    sabores = db.Column(db.Text, nullable=True)
    frase_botao = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(100), nullable=True)
    media_avaliacao = db.Column(db.Float, default=5.0)
    total_avaliacoes = db.Column(db.Integer, default=0)
    def __repr__(self):
        return f'<Produto {self.nome}>'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha_hash = db.Column(db.String(200), nullable=False)
    
    # CPF
    cpf = db.Column(db.String(14), nullable=True, unique=True)

    # Endereço completo
    cep = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(150), nullable=False)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    tipo_residencia = db.Column(db.String(20), nullable=False)  # 'casa' ou 'apartamento'
    numero = db.Column(db.String(20), nullable=False)  # número da casa ou bloco/apto
    complemento = db.Column(db.String(100), nullable=True)

    # Foto do usuário
    imagem = db.Column(db.String(100), nullable=True, default='default-avatar.png')

    # Validação de email
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email inválido!")
        return email

    # Setter para senha
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    # Verifica senha
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.nome}>"
