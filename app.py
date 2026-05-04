import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-padrao')

uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario_inserido = request.form.get('usuario')
    senha_inserida = request.form.get('senha')
    user = Usuario.query.filter_by(username=usuario_inserido).first()

    if user and user.senha == senha_inserida:
        return f"Bem-vindo, {user.nome}! Acesso ao Sanctum autorizado."
    else:
        # Mudança estratégica: use flash e redirecione
        flash("Usuário ou senha inválidos.", "error")
        return redirect(url_for('index'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    usuario_novo = request.form.get('usuario')
    senha_nova = request.form.get('senha')
    confirmar_senha = request.form.get('confirmar_senha')

    if not all([nome, email, usuario_novo, senha_nova]):
        flash("Preencha todos os campos!", "error")
        return redirect(url_for('cadastro'))

    if senha_nova != confirmar_senha:
        flash("As senhas não coincidem!", "error")
        return redirect(url_for('cadastro'))

    existe = Usuario.query.filter((Usuario.username == usuario_novo) | (Usuario.email == email)).first()
    if existe:
        flash("Usuário ou E-mail já cadastrados no sistema!", "warning")
        return redirect(url_for('cadastro'))

    novo_user = Usuario(nome=nome, email=email, username=usuario_novo, senha=senha_nova)
    
    try:
        db.session.add(novo_user)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao salvar: {e}", "error")
        return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True)