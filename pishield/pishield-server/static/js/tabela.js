function renderizarTabela() {
    let tabela = document.querySelector('main tbody');
    let aviso = document.querySelector('main > p');

    tabela.innerHTML = '';
    
    if (!clientes.length) {
        tabela.parentElement.style.display = 'none';
        aviso.style.display = 'block';
        return;
    }

    tabela.parentElement.style.display = 'table';
    aviso.style.display = 'none';

    for (cliente of clientes) {
        let tr = document.createElement('tr');
        
        let tdEthernet = document.createElement('td');
        tdEthernet.textContent = cliente.endereco_ethernet;

        let tdWifi = document.createElement('td');
        tdWifi.textContent = cliente.endereco_wifi;

        let tdData = document.createElement('td');
        tdData.textContent = cliente.data;

        let tdBotao = document.createElement('td');
        let botao = document.createElement('button')
        let botaoSpan = document.createElement('span');
        botaoSpan.textContent = 'delete';
        botaoSpan.classList.add('material-symbols-outlined');

        botao.addEventListener('click', () => {
            abrirModalConfirmacao(
                'Tem certeza de que deseja deletar o cliente?',
                'Ação pode ser irreversível.',
                async () => {
                    let resposta = await fetch(`/api/clientes/${cliente._id}`, {
                        method: 'DELETE'
                    });

                    let respostaJSON = await resposta.json();

                    abrirModalStatus(respostaJSON.ok, respostaJSON.mensagem);

                    carregarClientes();
                }
            ) 
        });

        botao.appendChild(botaoSpan);
        tdBotao.appendChild(botao);

        tr.appendChild(tdEthernet);
        tr.appendChild(tdWifi);
        tr.appendChild(tdData);
        tr.appendChild(tdBotao);

        tabela.appendChild(tr);
    }
}