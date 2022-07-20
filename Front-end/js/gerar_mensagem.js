$(function () {

    $(document).on("click", "#gerar_mensagem", function () {

        var fd = new FormData();
        
        var imagem = $('#imagem')[0].files;
        var texto = $("#texto")[0].files
        
        if (imagem.length > 0){
            fd.append('imagem', imagem[0]);
        }

        if (texto.length > 0){
            fd.append('texto', texto[0]);
        }

        $.ajax({
            url: 'http://localhost:5001/upload_gerar',
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

                $("#opcoes").append(`
                    <form>
                        <label for="campoChave">Chave Criptografica: </label>
                        <input id="chave_criptografica" type=number name=campoChave>
                        <br>
                        <button id="criar_mensagem" type="button" onClick="return false;">Gerar</button>
                    </form>
                `);
            }
            else {
                alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
            }
        }
    });

    $(document).on("click", "#criar_mensagem", function () {

        var chave = $("#chave_criptografica").val();

        $.ajax({
            url: `http://localhost:5001/gerar_mensagem/${chave}`,
            type: 'GET',
            contentType: 'application/json',
            success: gerarMensagemOk,
            error: function (xhr, status, error) {
                alert("Erro na conexão, verifique o backend. " + xhr.responseText + " - " + status + " - " + error);
            }
        });

        function gerarMensagemOk(retorno) {
            if (retorno.resultado == "ok"){
                alert("Mensagem Gerada!");
            }
            else {
                alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
            }
        }
    });
    
});