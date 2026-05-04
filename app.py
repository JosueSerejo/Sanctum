import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente (.env)
load_dotenv()

app = Flask(__name__)

# 2. Configurações de Segurança e Banco de Dados
# No Render, certifique-se de que SECRET_KEY e DATABASE_URL estejam configurados
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-padrao')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Inicialização do Banco de Dados
db = SQLAlchemy(app)

# 4. Definição do Modelo de Usuário
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# 5. Rotas da Aplicação

# Rota de Login (Página Inicial)
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario_inserido = request.form.get('usuario')
    senha_inserida = request.form.get('senha')

    user = Usuario.query.filter_by(username=usuario_inserido).first()

    # Validação simples conforme solicitado
    if user and user.senha == senha_inserida:
        return f"Bem-vindo, {user.username}! Acesso ao Sanctum autorizado."
    else:
        return "Usuário ou senha inválidos. Tente novamente.", 401

# Rota para exibir a página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota para processar o formulário de cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    usuario_novo = request.form.get('usuario')
    senha_nova = request.form.get('senha')

    # Validação básica
    if not usuario_novo or not senha_nova:
        return "Preencha todos os campos!", 400

    # Verifica se o usuário já existe no Postgres
    usuario_existe = Usuario.query.filter_by(username=usuario_novo).first()
    if usuario_existe:
        return "Este nome de usuário já está em uso.", 400

    # Criação do novo registro
    novo_user = Usuario(username=usuario_novo, senha=senha_nova)
    
    try:
        db.session.add(novo_user)
        db.session.commit()
        # Após cadastrar, redireciona para a tela de login
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return f"Erro ao salvar no banco de dados: {e}", 500

# 6. Inicialização do Servidor
if __name__ == '__main__':
    # Cria as tabelas no PostgreSQL se elas não existirem
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)