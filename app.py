from flask import Flask, render_template, request, redirect, url_for, session
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


# ------------------- ROTAS PRINCIPAIS -------------------


@app.route('/')
def index():
    if 'id' in session:
        return redirect(url_for('dashboard'))
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
        list_receitas = Receita.query.filter_by(id_usuario=session['id']).all()
        list_despesas = Despesa.query.filter_by(id_usuario=session['id']).all()

        total_receitas = 0.00
        total_despesas = 0.00

        for receita in list_receitas:
            total_receitas += float(receita.valor_receita)

        for despesa in list_despesas:
            total_despesas += float(despesa.valor_despesa)

        total_saldo = total_receitas - total_despesas

        return render_template('dashboard.html',
                               receitas=list_receitas,
                               despesas=list_despesas,
                               total_saldo=total_saldo,
                               total_receitas=total_receitas,
                               total_despesas=total_despesas)
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
        print("No senha:", user.senha, generate_password_hash(password))
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

    if float(preco) <= 0:
        return redirect(url_for("receitas"))

    nova_receita = Receita(id_usuario=session['id'], nome=nome, data_emissao=data, valor_receita=preco)
    db.session.add(nova_receita)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/adicionar_despesa', methods=['POST'])
def adicionar_despesa():
    nome = request.form['nome']
    data = request.form['data']
    preco = request.form['preco']

    if float(preco) <= 0:
        return redirect(url_for("despesas"))

    nova_despesa = Despesa(id_usuario=session['id'], nome=nome, data_emissao=data, valor_despesa=preco)
    db.session.add(nova_despesa)
    db.session.commit()

    return redirect(url_for('dashboard'))


# ----------------------- APP ---------------------


if __name__ == '__main__':
    app.run(debug=True)
