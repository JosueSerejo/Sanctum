document.addEventListener('DOMContentLoaded', function() {
    // Seleção de Elementos
    const loginForm = document.getElementById('login-form');
    const authSection = document.getElementById('auth-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const playlistList = document.getElementById('playlist-list');
    
    // Selecionamos o header que está fora das sections
    const mainHeader = document.querySelector('.login-header');

    /* ==========================================================================
       1. GERENCIAMENTO DE ALERTAS (INICIAL E DINÂMICO)
       ========================================================================== */
    function configurarAlerta(alerta) {
        setTimeout(function() {
            alerta.classList.add('fade-out');
            setTimeout(function() {
                alerta.remove();
            }, 500);
        }, 3000);
    }

    // Inicializa alertas que já vieram do Flask (via Jinja2)
    const alertasIniciais = document.querySelectorAll('.alert');
    alertasIniciais.forEach(configurarAlerta);

    // Função para criar novos alertas via JS (SPA)
    function mostrarAlerta(msg, tipo) {
        const container = document.getElementById('flash-container');
        if (!container) return;

        const alerta = document.createElement('div');
        alerta.className = `alert alert-${tipo}`;
        alerta.textContent = msg;
        container.appendChild(alerta);
        
        configurarAlerta(alerta);
    }

    /* ==========================================================================
       2. LÓGICA DE LOGIN (SPA)
       ========================================================================== */
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    // SUCESSO: Esconde a Logo (Header) e a Seção de Auth
                    if (mainHeader) mainHeader.style.display = 'none';
                    authSection.style.display = 'none';
                    
                    // Mostra o Dashboard
                    dashboardSection.style.display = 'block';
                    
                    carregarPlaylists(); 
                } else {
                    mostrarAlerta(data.message, 'danger');
                }
            } catch (error) {
                mostrarAlerta('Erro de conexão com o servidor.', 'danger');
            }
        });
    }

    /* ==========================================================================
       3. GESTÃO DE PLAYLISTS (MOCKUP)
       ========================================================================== */
    function carregarPlaylists() {
        const playlistsMock = [
            { id: 1, nome: 'Missa de Domingo - 19h' },
            { id: 2, nome: 'Casamento Lucas & Ana' },
            { id: 3, nome: 'Adoração Quinta-Feira' }
        ];

        if (!playlistList) return;

        playlistList.innerHTML = '';
        
        playlistsMock.forEach(pl => {
            const li = document.createElement('li');
            li.className = 'playlist-item';
            li.innerHTML = `
                <span>${pl.nome}</span>
                <i class="fas fa-chevron-right"></i>
            `;
            li.onclick = () => alert(`Abrindo: ${pl.nome}`);
            playlistList.appendChild(li);
        });
    }
});