const modalConfirmacao = document.querySelector('#modal-confirmacao');

modalConfirmacao.querySelector('.fechar').addEventListener('click', async () => {
    await fecharModalConfirmacao(false);
});

modalConfirmacao.querySelector('.confirmar').addEventListener('click', async () => {
    await fecharModalConfirmacao(true);
});

function abrirModalConfirmacao(titulo, texto, callback, ...parametros) {
    modalConfirmacao.style.visibility = 'visible';
    modalConfirmacao.style.opacity = '1';

    modalConfirmacao.querySelector('h3').textContent = titulo;
    modalConfirmacao.querySelector('p').textContent = texto;

    let botaoConfirmacao = modalConfirmacao.querySelector('.confirmar');

    botaoConfirmacao.replaceWith(botaoConfirmacao.cloneNode(true));

    let novoBotaoConfirmacao = modalConfirmacao.querySelector('.confirmar');
    
    novoBotaoConfirmacao.addEventListener('click', () => {
        if (callback) callback(...parametros);
        fecharModalConfirmacao();
    });
}

async function fecharModalConfirmacao() {
    modalConfirmacao.style.opacity = '0';
    setTimeout(() => {
        modalConfirmacao.style.visibility = 'hidden';
    }, 300);
}
