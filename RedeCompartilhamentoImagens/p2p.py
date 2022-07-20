from servidorArquivos import *
from clienteArquivos import *

def main():
    
    endereco_servidor_meta = ENDERECO_SERVIDOR_META
    endereco_servidor_arq = requests.get(f"http://{endereco_servidor_meta}/getServerIP",headers={}).json()["SERVER_IP"]

    if endereco_servidor_arq == "0":          
        servidor = Servidor()
    else:
        cliente = Cliente()

if __name__ == "__main__":
    main()