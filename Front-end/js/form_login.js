$(function () {

    $(document).on("click", "#btLogin", function () {

        login = $("#campoLogin").val();
        senha = $("#campoSenha").val();
        
        var dados = JSON.stringify({ login: login, senha: senha });

        $.ajax({
            url: 'http://localhost:5001/login',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: dados,
            success: loginOk,
            error: function (xhr, status, error) {
                alert("Erro na conexão, verifique o backend. " + xhr.responseText + " - " + status + " - " + error);
            }
        });
        
        function loginOk(retorno) {
            if (retorno.resultado == "ok") {
                sessionStorage.setItem('login', login);
                window.location = 'index.html';
            } 
            else {
                alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
            }
        }
    });   

});