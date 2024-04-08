from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'chave_boa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cashcontrol'
db = SQLAlchemy()


# ---------------------- CLASSES ------------------------


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    rg = db.Column(db.String(20))
    cpf = db.Column(db.String(14))
    banco = db.Column(db.String(50))
    agencia = db.Column(db.String(10))
    conta = db.Column(db.String(20))
    senha = db.Column(db.String(30))


class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # nome
    # data_emissao
    # valor_receitas


class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


# ------------------- ROTAS PRINCIPAIS -------------------


@app.route('/')
def index():
    return 'Hello World!'


# ------------------- ROTAS INTERMEDIARIAS -----------------


# a


# ----------------------- APP ---------------------


if __name__ == '__main__':
    app.run(debug=True)
