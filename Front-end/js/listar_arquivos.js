$(function () {

    $.ajax({
        url: 'http://localhost:5001/listar_arquivos',
        type: 'GET',
        contentType: 'application/json',
        success: listarArquivos,
        error: function (xhr, status, error) {
            alert("Erro na conexão, verifique o backend. " + xhr.responseText + " - " + status + " - " + error);
        }
    });

    function listarArquivos(retorno) {
        if (retorno.resultado == "ok") {
            if (retorno.detalhes == "None"){
                $("#listagem").html(`Nenhum Arquivo Disponível no Servidor de Arquivos`);
            }
            else {
                const arquivos = retorno.detalhes.split("/");
                
                for (i = 0; i < arquivos.length; i++) {
                        
                    $("#listagem").append(`
                        ${arquivos[i]} 
                        <button id="${arquivos[i]}" class="download_imagem" type="button" onClick="return false;">Download</button>
                        <br>
                    `);
                }
            }
        } 
        else {
            alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
        }
    }

    $(document).on("click", ".download_imagem", function () {

        eu = $(this).attr('id');

        $.ajax({
            url: `http://localhost:5001/download/${eu}`,
            type: 'GET',
            contentType: 'application/json',
            success: donwloadOk,
            error: function (xhr, status, error) {
                alert("Erro na conexão, verifique o backend. " + xhr.responseText + " - " + status + " - " + error);
            }
        });

        function donwloadOk(retorno) {
            if (retorno.resultado == "ok") {
                alert("Imagem baixada no diretório Downloads!")
            } 
            else {
                alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
            }
        }
    });
    
});