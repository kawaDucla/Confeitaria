from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from flask_login import UserMixin
import re
from app import db, login_manager
from flask_login import UserMixin

# =========================
# PRODUTO
# =========================
class Produto(db.Model):
    __tablename__ = 'produto'

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

# =========================
# USUÁRIO (FLASK-LOGIN)
# =========================
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), nullable=False, unique=True)
    senha_hash = db.Column(db.String(200), nullable=False)

    cpf = db.Column(db.String(14), nullable=True, unique=True)

    # Endereço
    cep = db.Column(db.String(10), nullable=False)
    rua = db.Column(db.String(150), nullable=False)
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))

    tipo_residencia = db.Column(db.String(20), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(100))

    imagem = db.Column(
        db.String(100),
        default='default-avatar.png'
    )

    pedidos = db.relationship(
        'Pedido',
        backref='usuario',
        lazy=True
    )

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email inválido")
        return email

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

# 🔐 FLASK-LOGIN USER LOADER
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# =========================
# PEDIDO
# =========================
class Pedido(db.Model):
    __tablename__ = 'pedido'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id'),
        nullable=False
    )

    total = db.Column(db.Float, nullable=False)

    forma_pagamento = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default='Aguardando pagamento'
    )

    data = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # PIX / MERCADO PAGO
    pix_payment_id = db.Column(db.String(120))
    pix_qr_code = db.Column(db.Text)
    pix_qr_code_base64 = db.Column(db.Text)

    itens = db.relationship(
        'ItemPedido',
        backref='pedido',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Pedido #{self.id}>'

# =========================
# ITEM DO PEDIDO
# =========================
class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey('pedido.id'),
        nullable=False
    )

    produto_nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<ItemPedido {self.produto_nome}>'
@login_manager.user_loader
def load_user(user_id):
    from app.models import Usuario
    return Usuario.query.get(int(user_id))
