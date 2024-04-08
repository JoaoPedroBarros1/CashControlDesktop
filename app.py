from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
app = Flask(__name__)


# ---------------------- CLASSES ------------------------


# ------------------- ROTAS PRINCIPAIS -------------------


@app.route('/')
def index():
    return 'Hello World!'


# ------------------- ROTAS INTERMEDIARIAS -----------------


if __name__ == '__main__':
    app.run(debug=True)
