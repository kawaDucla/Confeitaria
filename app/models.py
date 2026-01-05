from app import db

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

    def __repr__(self):
        return f'<Produto {self.nome}>'
