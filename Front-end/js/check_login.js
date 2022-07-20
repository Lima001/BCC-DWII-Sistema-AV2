$(function () {

    var login = sessionStorage.getItem('login');
    var mensagem = "";

    if (login === null) {
        mensagem = `Faça seu <a href=form_login.html>Login</a>!`;
    } 
    else {
        mensagem = `Logado: ${login}`;

        $("#menu").html(`
            Opções:
            <a href="index.html">Início</a> | 
            <a href="listar_arquivos.html">Listar Mensagens</a> |
            <a href="gerar_mensagem.html">Gerar Mensagem</a> |
            <a href="decifrar_mensagem.html">Decifrar Mensagem</a>
            <a href=# id="linkLogout">Logout</a>
        `);
    }

    $("#mensagem").html(mensagem);

    $(document).on("click", "#linkLogout", function () {
        sessionStorage.removeItem('login');
        window.location = 'index.html';
    });

});