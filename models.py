from main import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))


class Receita(db.Model):
    id_receita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(255))
    data_emissao = db.Column(db.Date)
    valor_receita = db.Column(db.Numeric(10, 2))


class Despesa(db.Model):
    id_despesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(255))
    data_emissao = db.Column(db.Date)
    valor_despesa = db.Column(db.Numeric(10, 2))
