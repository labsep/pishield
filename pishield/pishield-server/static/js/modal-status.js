const modalStatus = document.querySelector('#modal-status');

modalStatus.querySelector('.fechar').addEventListener('click', () => {
    fecharModalStatus();
});

function abrirModalStatus(status, mensagem) {
    if (modalStatus.style.visibility == 'visible') {
        return;
    }

    modalStatus.style.visibility = 'visible';
    modalStatus.style.opacity = '1';
    modalStatus.querySelector('.container span:first-child').textContent = status ? 'check_circle' : 'error';
    modalStatus.querySelector('.container span:first-child').style.color = status ? 'green' : '#802020';
    modalStatus.querySelector('.container .texto-modal h5').textContent = status ? 'Ok' : 'Erro';
    modalStatus.querySelector('.container .texto-modal p').textContent = mensagem;

    setTimeout(fecharModalStatus, 3000);
}

function fecharModalStatus() {
    modalStatus.style.opacity = '0';
    setTimeout(() => {
        modalStatus.style.visibility = 'hidden';
    }, 500);
}