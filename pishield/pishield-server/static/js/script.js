let clientes = [];

document.addEventListener('DOMContentLoaded', carregarClientes);

document.querySelector('.adicionar').addEventListener('click', () => {
    abrirModal();
});
