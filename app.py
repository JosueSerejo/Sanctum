import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente (.env)
load_dotenv()

app = Flask(__name__)

# 2. Configurações de Segurança e Banco de Dados
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-padrao')

# Correção automática para URLs do Neon/PostgreSQL
uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Inicialização do Banco de Dados
db = SQLAlchemy(app)

# 4. Definição do Modelo de Usuário
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# Garantir que as tabelas existam no Neon ao iniciar
with app.app_context():
    db.create_all()

# 5. Rotas da Aplicação

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario_inserido = request.form.get('usuario')
    senha_inserida = request.form.get('senha')

    user = Usuario.query.filter_by(username=usuario_inserido).first()

    if user and user.senha == senha_inserida:
        return f"Bem-vindo, {user.username}! Acesso ao Sanctum autorizado."
    else:
        return "Usuário ou senha inválidos. Tente novamente.", 401

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    usuario_novo = request.form.get('usuario')
    senha_nova = request.form.get('senha')

    if not usuario_novo or not senha_nova:
        return "Preencha todos os campos!", 400

    usuario_existe = Usuario.query.filter_by(username=usuario_novo).first()
    if usuario_existe:
        return "Este nome de usuário já está em uso.", 400

    novo_user = Usuario(username=usuario_novo, senha=senha_nova)
    
    try:
        db.session.add(novo_user)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao salvar no banco de dados: {e}", 500

# 6. Inicialização (para rodar localmente)
if __name__ == '__main__':
    app.run(debug=True)