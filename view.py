from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import generate_password_hash, check_password_hash
from main import app, db
from models import Usuario, Receita, Despesa


# ------------------- ROTAS PRINCIPAIS -------------------


@app.route('/')
def index():
    if 'id' not in session:
        return render_template('home.html')

    return redirect(url_for('dashboard'))


@app.route('/login')
def login_form():
    if 'id' not in session:
        return render_template('login.html')

    return redirect(url_for('dashboard'))


@app.route('/cadastro')
def cadastro_form():
    if 'id' not in session:
        return render_template('cadastro.html')

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect(url_for('index'))

    list_receitas = Receita.query.filter_by(id_usuario=session['id']).all()
    list_despesas = Despesa.query.filter_by(id_usuario=session['id']).all()

    total_receitas = 0.00
    total_despesas = 0.00

    for receita in list_receitas:
        total_receitas += float(receita.valor_receita)

    for despesa in list_despesas:
        total_despesas += float(despesa.valor_despesa)

    total_receitas = round(total_receitas, 2)
    total_despesas = round(total_despesas, 2)
    total_saldo = round((total_receitas - total_despesas), 2)

    return render_template('dashboard.html',
                           receitas=list_receitas,
                           despesas=list_despesas,
                           total_saldo=total_saldo,
                           total_receitas=total_receitas,
                           total_despesas=total_despesas)


@app.route('/receitas')
def receitas():
    if 'id' not in session:
        return redirect(url_for('index'))

    return render_template('receitas.html')


@app.route('/despesas')
def despesas():
    if 'id' not in session:
        return redirect(url_for('index'))

    return render_template('despesas.html')


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
    if 'id' not in session:
        return redirect(url_for('index'))

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
    else:
        flash('Email já está em uso. Por favor, escolha outro email.', 'error')
        return redirect(url_for('cadastro_form'))


@app.route('/adicionar_receita', methods=['POST'])
def adicionar_receita():
    if 'id' not in session:
        return redirect(url_for('index'))

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
    if 'id' not in session:
        return redirect(url_for('index'))

    nome = request.form['nome']
    data = request.form['data']
    preco = request.form['preco']

    if float(preco) <= 0:
        return redirect(url_for("despesas"))

    nova_despesa = Despesa(id_usuario=session['id'], nome=nome, data_emissao=data, valor_despesa=preco)
    db.session.add(nova_despesa)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/receitas/<int:id_receita>', methods=['PUT'])
def put_receita(id_receita):
    if 'id' not in session:
        return redirect(url_for('index'))

    receita = Receita.query.get(id_receita)

    if receita:
        data = request.json
        receita.nome = data.get('nome', receita.nome)
        receita.data_emissao = data.get('data_emissao', receita.data_emissao)
        receita.valor_receita = data.get('valor_receita', receita.valor_receita)

        db.session.commit()

    redirect(url_for('dashboard'))


@app.route('/receitas/<int:id_receita>', methods=['DELETE'])
def delete_receita(id_receita):
    if 'id' not in session:
        return redirect(url_for('index'))

    receita = Receita.query.get(id_receita)

    if receita:
        db.session.delete(receita)
        db.session.commit()

    redirect(url_for('dashboard'))


@app.route('/despesas/<int:id_despesa>', methods=['PUT'])
def put_despesa(id_despesa):
    if 'id' not in session:
        return redirect(url_for('index'))

    despesa = Receita.query.get(id_despesa)

    if despesa:
        data = request.json
        despesa.nome = data.get('nome', despesa.nome)
        despesa.data_emissao = data.get('data_emissao', despesa.data_emissao)
        despesa.valor_receita = data.get('valor_receita', despesa.valor_receita)

        db.session.commit()

    redirect(url_for('dashboard'))


@app.route('/despesas/<int:id_despesa>', methods=['DELETE'])
def delete_despesa(id_despesa):
    if 'id' not in session:
        return redirect(url_for('index'))

    despesa = Receita.query.get(id_despesa)

    if despesa:
        db.session.delete(despesa)
        db.session.commit()

    redirect(url_for('dashboard'))
