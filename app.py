import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# 1. Carrega as variáveis localmente
load_dotenv()

app = Flask(__name__)

# 2. Configurações de Segurança e Banco de Dados
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Inicialização do Banco de Dados
db = SQLAlchemy(app)

# 4. Definição do Modelo de Usuário (Tabela no Postgres)
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# 5. Rotas da Aplicação
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Pega os nomes dos campos definidos no atributo 'name' do HTML
    usuario_inserido = request.form.get('usuario')
    senha_inserida = request.form.get('senha')

    # Busca no banco de dados online
    user = Usuario.query.filter_by(username=usuario_inserido).first()

    # Validação simples (comparação direta)
    if user and user.senha == senha_inserida:
        # Aqui você poderia redirecionar para a dashboard do Sanctum futuramente
        return f"Bem-vindo, {user.username}! Acesso ao Sanctum autorizado."
    else:
        # Retorna uma mensagem simples em caso de erro
        return "Usuário ou senha inválidos. Tente novamente.", 401

# 6. Inicialização do Servidor
if __name__ == '__main__':
    # Garante que as tabelas existam no banco do Render antes de rodar o app
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)