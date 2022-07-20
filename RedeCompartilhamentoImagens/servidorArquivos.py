from config import ENDERECO_SERVIDOR_ARQUIVOS
from config import PORTA_SERVIDOR_ARQUIVOS
from config import ENDERECO_SERVIDOR_META
from config import TAMANHO_MAX_IMAGEM
from config import TAMANHO_MAX_MENSAGEM
from config import FORMATO
from config import DIRETORIO_SERVIDOR_ARQUIVOS

import socket
import requests 
import threading 
import sys

from os import listdir
from os.path import isfile, join, exists

class Servidor:

    def __init__(self):
        self.conexoes = []
        self.pontos = []
        self.socket = None

        self.iniciar_servidor()

    def iniciar_servidor(self):
        print("Iniciando Servidor...")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((ENDERECO_SERVIDOR_ARQUIVOS, PORTA_SERVIDOR_ARQUIVOS))
        self.socket.listen()

        self.contactar_servidor_web()
        self.executar_servidor()

    def contactar_servidor_web(self):   
        resp = requests.get(f"http://{ENDERECO_SERVIDOR_META}/setServerIP/{ENDERECO_SERVIDOR_ARQUIVOS}",headers={}).json()
        print(f"Endereço Servidor de Arquivos: {resp['SERVER_IP']}")

    def executar_servidor(self):
        print("Aguardando por Conexões")
        try:
            while True:

                conexao, endereco = self.socket.accept()
                self.pontos.append(endereco)
                self.conexoes.append(conexao)

                print(f"{endereco} conectado!")
        
                thread_conexao = threading.Thread(target=self.handler, args=(conexao, endereco))
                thread_conexao.start()
        
        except KeyboardInterrupt as e:
            print("Encerrando Servidor executar_servidor()...")
            self.encerrar_servidor()
            sys.exit()

    def handler(self, conexao, endereco):

        try:
            while True:            
                
                dados = conexao.recv(TAMANHO_MAX_MENSAGEM).decode(FORMATO).split("$")
                
                print(f"{endereco} enviou o comando {dados[0]}")

                if dados[0] == "LIST":
                    self.executar_listar(conexao, endereco)

                elif dados[0] == "DISCONNECT":
                    self.desconectar(conexao, endereco)
                    break

                elif dados[0] == "NEW_CLIENT":
                    if dados[1] == "1":
                        self.enviar_todos_arquivos(conexao, endereco)
                    else:
                        conexao.send("OK".encode(FORMATO))

                elif dados[0] == "HELP":
                    self.enviar_ajuda(conexao, endereco)

                elif dados[0] == "DOWNLOAD":
                    self.enviar_unico_arquivo(conexao, endereco, dados[1])

                elif dados[0] == "UPLOAD":
                    self.realizar_upload(conexao, endereco, dados[1])

                else:
                    conexao.send("None".encode(FORMATO))
              
        except KeyboardInterrupt as e:
            print("Encerrando Servidor handler()...")
            conexao.close()
            sys.exit()
        
        except Exception as e:
            sys.exit()


    def executar_listar(self, conexao, endereco):
        arquivos = [f for f in listdir(DIRETORIO_SERVIDOR_ARQUIVOS) if isfile(join(DIRETORIO_SERVIDOR_ARQUIVOS, f))]
        
        if arquivos == []:
            conexao.send("None".encode(FORMATO))
            return
        
        conexao.send("/".join(arquivos).encode(FORMATO))
        return

    def desconectar(self, conexao, endereco):
        conexao.send("DISCONNECTED".encode(FORMATO))
        
        print(f"{endereco} disconectado")
        
        self.conexoes.remove(conexao)
        self.pontos.remove(endereco)
        conexao.close()
        return

    def enviar_todos_arquivos(self, conexao, endereco):
        arquivos = [f for f in listdir(DIRETORIO_SERVIDOR_ARQUIVOS) if isfile(join(DIRETORIO_SERVIDOR_ARQUIVOS, f))]
        
        if arquivos == []:
            conexao.send("None".encode(FORMATO))
            return
        
        for arq in arquivos:
            print(f"Enviando arquivo {arq} para {endereco}")
            conexao.send(f"RECEIVE_FILE${arq}".encode(FORMATO))
            
            dados_arquivo = None
            with open(join(DIRETORIO_SERVIDOR_ARQUIVOS, arq), "rb") as arq:
                dados_arquivo = arq.read()
            
            conexao.send(dados_arquivo)
            conexao.recv(TAMANHO_MAX_MENSAGEM)

        conexao.send("OK".encode(FORMATO))
        print(f"Todos os arquivos foram enviados para {endereco}!")
        return

    def enviar_ajuda(self, conexao, endereco):
        mensagem = ""
        mensagem += "LIST                        -> Retorna a lista dos arquivos presentes no diretório do servidor\n"
        mensagem += "DOWNLOAD$<arquivo>          -> Cliente deseja realizar o download de <arquivo> do servidor\n"
        mensagem += "UPLOAD$<arquivo>            -> Cliente deseja realizar o upload de <arquivo> para o servidor\n"
        mensagem += "DISCONNECT                  -> Cliente deseja desconectar do Servidor\n"
        mensagem += "NEW_CLIENT$<0|1>            -> Novo cliente conectou na rede. Verificar se é necessário enviar\n"
        mensagem += "                               todos os arquivos do diretorio do servidor, ou não.\n"
        mensagem += "                               0 - Não enviar arquivos ao cliente\n"
        mensagem += "                               1 - Enviar todos os arquivos ao cliente\n"
        mensagem += "HELP                        -> Exibe a lista de comandos aceitos\n"

        conexao.send(mensagem.encode(FORMATO))
        return

    def enviar_unico_arquivo(self, conexao, endereco, nome_arquivo):
        print(f"{endereco} requisitando {nome_arquivo}")
        
        if not exists(join(DIRETORIO_SERVIDOR_ARQUIVOS, nome_arquivo)):
            conexao.send("None".encode(FORMATO))
            print(f"Arquivo {nome_arquivo} Inexistente - Impossível enviar para {endereco}")
            return

        conexao.send(f"RECEIVE_FILE${nome_arquivo}".encode(FORMATO))

        dados_arquivo = None
        with open(join(DIRETORIO_SERVIDOR_ARQUIVOS, nome_arquivo), "rb") as arq:
            dados_arquivo = arq.read()
    
        conexao.send(dados_arquivo)
        conexao.recv(TAMANHO_MAX_MENSAGEM)
        print(f"Arquivo {nome_arquivo} enviado para {endereco}")
        return

    def realizar_upload(self, conexao, endereco, nome_arquivo):
        print(f"Recebendo arquivo {nome_arquivo} de {endereco}")

        dados_arquivo = conexao.recv(TAMANHO_MAX_IMAGEM)
        with open(f"{DIRETORIO_SERVIDOR_ARQUIVOS}/{nome_arquivo}", "wb") as file:
            file.write(dados_arquivo)

        print(f"Arquivo {nome_arquivo} recebido de {endereco}")
        conexao.send("OK".encode(FORMATO))

        for i in range(len(self.conexoes)):
            if self.conexoes[i] != conexao:
                self.conexoes[i].send(f"RECEIVE_FILE${nome_arquivo}".encode(FORMATO))
                self.conexoes[i].send(dados_arquivo)
                self.conexoes[i].recv(TAMANHO_MAX_MENSAGEM)
                print(f"Arquivo {nome_arquivo} enviado para {self.pontos[i]}")

        return

    def encerrar_servidor(self):
        for c in self.conexoes:
            c.close()

        requests.get(f"http://{self.endereco_servidor_web}/setServerIP/0",headers={}).json()
        return