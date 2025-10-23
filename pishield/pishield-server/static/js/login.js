document.querySelector('button').addEventListener('click', async () => {
    let senha = document.querySelector('input').value;

    let resposta = await fetch('/login', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'senha': senha
        })
    });

    let respostaJSON = await resposta.json();

    abrirModalStatus(respostaJSON.ok, respostaJSON.mensagem);

    if (respostaJSON.ok) {
        window.location.href = '/';
    }
});