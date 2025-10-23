const modal = document.querySelector('#modal');

modal.querySelector('.fechar').addEventListener('click', () => {
    fecharModal();
});

function abrirModal() {
    modal.style.visibility = 'visible';
    modal.style.opacity = '1';
}

function fecharModal() {
    modal.style.opacity = '0';
    setTimeout(() => {
        modal.style.visibility = 'hidden';
    }, 300);
}