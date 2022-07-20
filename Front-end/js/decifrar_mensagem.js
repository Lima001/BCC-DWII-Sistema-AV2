$(function () {

    $(document).on("click", "#enviar_imagem", function () {

        var fd = new FormData();
        var imagem = $('#imagem')[0].files;
        
        if (imagem.length > 0){
            fd.append('imagem', imagem[0]);
        }


        $.ajax({
            url: 'http://localhost:5001/upload_recuperar',
            type: 'POST',
            processData: false,
            contentType: false,
            data: fd,
            success: uploadOk,
            error: function (xhr, status, error) {
                alert("Erro na conexão, verifique o backend. " + xhr.responseText + " - " + status + " - " + error);
            }
        });
        function uploadOk(retorno){
            if (retorno.resultado == "ok"){
                var html = `
                    <form>
                        <label for="campoChave">Chave Criptografica: </label>
                        <input id="chave_criptografica" type=number name=campoChave>
                        <br>
                        <button id="recuperar_mensagem" type="button" onClick="return false;">Recuperar</button>
                    </form>
                `;
                $("#opcoes").append(html);
            }
            else {
                alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
            }
        }
    });

    $(document).on("click", "#recuperar_mensagem", function () {
        
        var chave = $("#chave_criptografica").val();
    
        $.ajax({
            url: `http://localhost:5001/recuperar_mensagem/${chave}`,
            type: 'GET',
            contentType: 'application/json',
            success: recuperarMensagemOk,
            error: function (xhr, status, error) {
                alert("Erro na conexão, verifique o backend. " + xhr.responseText + " - " + status + " - " + error);
            }
        });
        function recuperarMensagemOk(retorno) {
            if (retorno.resultado == "ok"){
                html = `<a href="../ServidorWeb/${retorno.detalhes}">Mensagem Recuperada<\a>`
                $("#opcoes").append(html);
            }
            else {
                alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
            }
        }
    });
});