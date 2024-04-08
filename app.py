from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'chave_boa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cashcontrol'
db = SQLAlchemy(app)


# ---------------------- CLASSES ------------------------


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(30))


class Receita(db.Model):
    id_receita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    data_emissao = db.Column(db.Date)
    valor_receita = db.Column(db.Numeric(10, 2))


class Despesa(db.Model):
    id_despesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    data_emissao = db.Column(db.Date)
    valor_despesa = db.Column(db.Numeric(10, 2))


# ------------------- ROTAS PRINCIPAIS -------------------


@app.route('/')
def index():
    if 'id' in session:
        return render_template(url_for('dashboard'))
    else:
        return render_template('home.html')


@app.route('/login')
def login_form():
    if 'id' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')


@app.route('/cadastro')
def cadastro_form():
    if 'id' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('cadastro.html')


@app.route('/dashboard')
def dashboard():
    if 'id' in session:
        return render_template('dashboard.html', email=session['email'])
    else:
        return redirect(url_for('index'))


@app.route('/receitas')
def receitas():
    if 'id' in session:
        return render_template('receitas.html')
    else:
        return redirect(url_for('index'))


@app.route('/despesas')
def despesas():
    if 'id' in session:
        return render_template('despesas.html')
    else:
        return redirect(url_for('index'))


# ------------------- ROTAS INTERMEDIARIAS -----------------


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Usuario.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for('login_form'))

    senha = check_password_hash(user.senha, password)
    if not senha:
        return redirect(url_for('login_form'))

    session['id'] = user.id
    return redirect(url_for('dashboard'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))


@app.route('/cadastro', methods=['POST'])
def cadastro_post():
    username = request.form['username']
    email = request.form['email']
    senha = request.form['password']

    user = Usuario.query.filter_by(email=email).first()
    if not user:
        senha_hash = generate_password_hash(senha).decode('utf-8')
        new_user = Usuario(
            nome=username, email=email,
            senha=senha_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return redirect(url_for('cadastro_form'))


@app.route('/adicionar_receita', methods=['POST'])
def adicionar_receita():
    nome = request.form['nome']
    data = request.form['data']
    preco = request.form['preco']

    nova_receita = Receita(nome=nome, data_emissao=data, valor_receitas=preco)
    db.session.add(nova_receita)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/adicionar_despesa', methods=['POST'])
def adicionar_despesa():
    nome = request.form['nome']
    data = request.form['data']
    preco = request.form['preco']

    nova_despesa = Despesa(nome=nome, data_emissao=data, valor_despesas=preco)
    db.session.add(nova_despesa)
    db.session.commit()

    return redirect(url_for('dashboard'))


# ----------------------- APP ---------------------


if __name__ == '__main__':
    app.run(debug=True)
