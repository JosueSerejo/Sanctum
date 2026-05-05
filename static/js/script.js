document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade-out');
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 3000);
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const authSection = document.getElementById('auth-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const playlistList = document.getElementById('playlist-list');

    // 1. Processar Login via AJAX
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
                    // Esconde login e mostra dashboard
                    authSection.style.display = 'none';
                    dashboardSection.style.display = 'block';
                    carregarPlaylists(); // Função para buscar listas do banco
                } else {
                    mostrarAlerta(data.message, 'danger');
                }
            } catch (error) {
                mostrarAlerta('Erro de conexão com o servidor.', 'danger');
            }
        });
    }

    // 2. Simulação de carregar playlists
    function carregarPlaylists() {
        const playlistsMock = [
            { id: 1, nome: 'Missa de Domingo - 19h' },
            { id: 2, nome: 'Casamento Lucas & Ana' },
            { id: 3, nome: 'Adoração Quinta-Feira' }
        ];

        playlistList.innerHTML = ''; // Limpa a lista
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

    // Função auxiliar para alertas na SPA
    function mostrarAlerta(msg, tipo) {
        const container = document.getElementById('flash-container');
        const alerta = document.createElement('div');
        alerta.className = `alert alert-${tipo}`;
        alerta.textContent = msg;
        container.appendChild(alerta);
        
        setTimeout(() => {
            alerta.classList.add('fade-out');
            setTimeout(() => alerta.remove(), 500);
        }, 3000);
    }
});