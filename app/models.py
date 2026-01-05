from app import db

class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo_sabor = db.Column(db.String(10), nullable=False)
    sabor_unico = db.Column(db.String(50))
    sabores = db.Column(db.Text)
    descricao = db.Column(db.Text, nullable=False)
    frase_botao = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(100))  # campo para o nome da imagem
