from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_bcrypt import Bcrypt


bcrypt=Bcrypt()


import os
from werkzeug.utils import secure_filename


from app import db, Bcrypt
from app.models import User, Livro


class UserForm (FlaskForm):
    nome = StringField ('Nome', validators=[DataRequired()])
    sobrenome = StringField ('Sobrenome', validators=[DataRequired()])
    email = StringField ('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já cadastrado.')


    def save (self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User (
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha.decode('utf-8')
        )


        db.session.add(user)
        db.session.commit()
        return (user)
   
class LoginForm (FlaskForm):
    email = StringField ('E-mail', validators=[DataRequired(),Email()])
    senha = PasswordField ('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')


    def login (self):
        # Recuperar o usuário do E-Mail
        user = User.query.filter_by (email=self.email.data).first()


        # Verificar se a senha é válida
        if user:
            if bcrypt.check_password_hash (user.senha, self.senha.data.encode ('utf-8')):
                # Retorna o usuário
                return user
            else:
                raise Exception ('Senha incorreta!')
           
        else:
            raise Exception ('Usuário não encontrado!')




class LivroForm (FlaskForm):
    autor = StringField ('Autor', validators=[DataRequired()])
    titulo = StringField ('Título', validators=[DataRequired()])
    ano_publicacao = IntegerField('Ano de Publicacão', validators=[DataRequired()])
    genero = StringField ('Gênero', validators=[DataRequired()])
    quantidade = IntegerField ('Quantidade', validators=[DataRequired()])
    btnSubmit = SubmitField('Cadastrar')


    def save (self):
        livro = Livro (
            titulo = self.titulo.data,
            autor = self.autor.data,
            ano_publicacao = self.ano_publicacao.data,
            genero = self.genero.data,
            quantidade = self.quantidade.data
        )
       
        db.session.add(livro)
        db.session.commit()
        return livro
   
    def update(self, livro):
        livro.autor = self.autor.data
        livro.titulo = self.titulo.data
        livro.ano_publicacao = self.ano_publicacao.data
        livro.genero = self.genero.data
        livro.quantidade = self.quantidade.data
        db.session.commit()
        return livro