# ⛪ Sanctum - Gestão de Repertório Litúrgico

O **Sanctum** é uma plataforma web robusta projetada para a organização e gestão de repertórios musicais para missas e celebrações litúrgicas. Desenvolvido sob a filosofia *Mobile First*, o sistema garante que músicos e ministérios tenham acesso instantâneo a playlists, letras e referências de áudio, mesmo durante a dinâmica das celebrações.

---

## 🌟 Diferenciais
- **Foco na Liturgia:** Organização baseada nos momentos específicos do rito (Entrada, Ato Penitencial, Glória, etc.).
- **Experiência do Usuário (UX):** Interface de alto contraste otimizada para ambientes com pouca ou muita iluminação (comum em igrejas).
- **Escalabilidade:** Backend preparado para expansão de funcionalidades e integração de APIs externas.

---

## 🚀 Funcionalidades Principais

### 🔒 Autenticação de Usuários
- Sistema de login e cadastro seguro com validação de dados.
- Feedback em tempo real via **Flash Messages** (sucesso, erro e avisos).
- Persistência de dados com tratamento de sessões.

### 🎵 Gestão de Conteúdo (Em Desenvolvimento)
- **Playlists Dinâmicas:** Criação e edição de listas de músicas por celebração.
- **Categorização Automática:** Filtros por momentos litúrgicos.
- **Player & Lyrics:** Visualizador de letras integrado com links diretos para referências no YouTube.

---

## 🛠️ Tecnologias & Arquitetura

O projeto utiliza uma stack moderna e serverless para garantir alta disponibilidade:

- **Linguagem:** Python
- **Framework Web:** Flask
- **Persistência de Dados:** SQLAlchemy com **PostgreSQL**
- **Frontend:** Jinja2 Templates, CSS3 e JavaScript.
- **Deploy & Infra:** [Vercel](https://vercel.com) (Serverless Functions)

---

## 📂 Estrutura do Repositório

```text
sanctum/
├── static/              # Arquivos estáticos
│   ├── css/
│   │   └── style.css    # Estilização customizada (Dark Gold Theme)
│   └── js/
│       └── script.js    # Lógica de alertas e interações UI
├── templates/           # Páginas HTML (Jinja2)
│   ├── login.html       # Tela de acesso
│   └── cadastro.html    # Tela de registro de novos usuários
├── app.py               # Servidor Flask e rotas
├── requirements.txt     # Dependências do projeto
├── vercel.json          # Configurações de deploy Vercel
└── .env.example         # Exemplo de variáveis de ambiente