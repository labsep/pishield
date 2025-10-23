document.querySelector('#modal .formulario button').addEventListener('click', async () => {
    let enderecoEthernet = document.getElementsByName('endereco-ethernet')[0].value;
    let enderecoWifi = document.getElementsByName('endereco-wifi')[0].value;

    let resposta = await fetch('/api/clientes', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'endereco_ethernet': enderecoEthernet,
            'endereco_wifi': enderecoWifi
        })
    });

    let respostaJSON = await resposta.json();

    abrirModalStatus(respostaJSON.ok, respostaJSON.mensagem);

    carregarClientes();
});

async function carregarClientes() {
    let resposta = await fetch('/api/clientes');

    let respostaJSON = await resposta.json();

    clientes = respostaJSON.clientes;

    renderizarTabela();
}