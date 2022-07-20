import socket
import sys

from os import mkdir
from random import randint

from config import ENDERECO_SERVIDOR_ARQUIVOS, PORTA_SERVIDOR_ARQUIVOS
from config import TAMANHO_MAX_IMAGEM, TAMANHO_MAX_MENSAGEM, FORMATO

class Cliente:

    def __init__(self):
        self.socket = None
        self.id = randint(0,10000)

        self.iniciar_cliente()

    def iniciar_cliente(self):
        print(f"Iniciando Cliente - ID: {self.id}")
        print("Preparando para conectar-se ao Servidor de Arquivos...")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.connect((ENDERECO_SERVIDOR_ARQUIVOS, PORTA_SERVIDOR_ARQUIVOS))

        mkdir(f"ArquivosCliente{self.id}")

        self.executar_cliente()

    def executar_cliente(self):
        print("Cliente conectado!")
        
        self.socket.send("NEW_CLIENT$1".encode(FORMATO))
        
        try:
            while True:            

                resposta = self.socket.recv(TAMANHO_MAX_MENSAGEM).decode(FORMATO)
                print(resposta)

                if resposta.split("$")[0] == "RECEIVE_FILE":
                    nome_arquivo = resposta.split("$")[1]

                    print(f"Recebendo arquivo {nome_arquivo}")
                    
                    dados_arquivo = self.socket.recv(TAMANHO_MAX_IMAGEM)
                    with open(f"ArquivosCliente{self.id}/{nome_arquivo}", "wb") as file:
                        file.write(dados_arquivo)

                    self.socket.send("OK".encode(FORMATO))


        except KeyboardInterrupt as e:
            print("Desconectando da rede P2P")
            
            self.socket.send("DISCONNECT".encode(FORMATO))
            resposta = self.socket.recv(TAMANHO_MAX_MENSAGEM).decode(FORMATO)
            
            print(resposta)
            sys.exit()