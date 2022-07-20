from email.mime import image
from genericpath import exists
import requests
import socket

from flask import *
from flask_cors import CORS
from werkzeug.utils import secure_filename

from os import listdir, mkdir, remove, getlogin, rmdir
from os.path import isfile, join

from random import randint
from hashlib import sha512
from time import sleep

from BibliotecasExtras.Criptografia.criptografia import *
from BibliotecasExtras.Esteganografia.esteganografia import *
from BibliotecasExtras.Pipe.pipeline import *

from config import DIRETORIO_UPLOAD
from config import LOGIN, SENHA
from config import ENDERECO_SERVIDOR_META, PORTA_SERVIDOR_ARQUIVOS, PORTA_SERVIDOR_WEB
from config import TAMANHO_MAX_IMAGEM, TAMANHO_MAX_MENSAGEM, FORMATO
from config import EXT_IMAGENS, EXT_TEXTO

app_servidor_web = Flask(__name__)

CORS(app_servidor_web)

app_servidor_web.config['DIRETORIO_UPLOAD'] = DIRETORIO_UPLOAD
app_servidor_web.config['MAX_CONTENT_LENGTH'] = TAMANHO_MAX_IMAGEM

arquivos = [f for f in listdir(DIRETORIO_UPLOAD) if isfile(join(DIRETORIO_UPLOAD, f))]

if arquivos != []:
    for f in arquivos:
        remove(join(DIRETORIO_UPLOAD, f))

if exists(DIRETORIO_UPLOAD):
    rmdir(DIRETORIO_UPLOAD)

mkdir(DIRETORIO_UPLOAD)

@app_servidor_web.route('/')
def iniciar():
    return "Backend Servidor Web Operante!"


@app_servidor_web.route("/login", methods=['POST'])
def login():
    resposta = jsonify({"resultado": "ok", "detalhes": "ok"})

    dados = request.get_json()  
    login = dados['login']
    senha = dados['senha']
    
    if sha512(login.encode("utf-8")).hexdigest() != LOGIN or sha512(senha.encode("utf-8")).hexdigest() != SENHA:
        resposta = jsonify({"resultado": "erro", "detalhes": "login e/ou senha invalido(s)"})
    
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta


@app_servidor_web.route("/listar_arquivos")
def listar_arquivos():
    requisicao = requests.get(f"http://{ENDERECO_SERVIDOR_META}/getServerIP",headers={})
    
    if requisicao.status_code != 200:
        resposta = jsonify({"resultado": "erro", "detalhes": "Impossível contactar servidor de metadados!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    
    end_serv_arq = requisicao.json()["SERVER_IP"]
    
    if end_serv_arq == "0":
        resposta = jsonify({"resultado": "erro", "detalhes": "Servidor de arquivos inoperante!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((end_serv_arq, PORTA_SERVIDOR_ARQUIVOS))

    s.send("LIST".encode(FORMATO))
    lista_arquivos = s.recv(TAMANHO_MAX_MENSAGEM).decode(FORMATO)

    s.send("DISCONNECT".encode(FORMATO))
    s.recv(TAMANHO_MAX_MENSAGEM)

    resposta = jsonify({"resultado": "ok", "detalhes": lista_arquivos})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta


@app_servidor_web.route("/gerar_mensagem/<chave>")
def gerar_mensagem(chave):
    
    chave = int(chave)
    
    if chave < 0 or chave > 26:
        resposta = jsonify({"resultado": "erro", "detalhes": "Chave inválida!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta

    imagem = [f for f in listdir(DIRETORIO_UPLOAD) if isfile(join(DIRETORIO_UPLOAD, f)) and "imagem" == f.split(".")[0]][0]
    random_n = randint(0,1000000)
    
    p = Pipeline()
    p.add_pipe(criptografar, (f"{DIRETORIO_UPLOAD}/texto.txt", f"{DIRETORIO_UPLOAD}/texto_criptografado.txt", chave))
    p.add_pipe(esteganografar, (f"{DIRETORIO_UPLOAD}/{imagem}", f"{DIRETORIO_UPLOAD}/imagem_{chave}{random_n}", f"{DIRETORIO_UPLOAD}/texto_criptografado.txt"))
    p.process()

    requisicao = requests.get(f"http://{ENDERECO_SERVIDOR_META}/getServerIP",headers={})
    
    if requisicao.status_code != 200:
        resposta = jsonify({"resultado": "erro", "detalhes": "Impossível contactar servidor de metadados!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    
    end_serv_arq = requisicao.json()["SERVER_IP"]
    
    if end_serv_arq == "0":
        resposta = jsonify({"resultado": "erro", "detalhes": "Servidor de arquivos inoperante!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((end_serv_arq, PORTA_SERVIDOR_ARQUIVOS))

    sleep(10)

    comando = f"UPLOAD$imagem_{chave}{random_n}.png"
    s.send(comando.encode(FORMATO))
    
    dados_arquivo = None
    with open(f"{DIRETORIO_UPLOAD}/imagem_{chave}{random_n}.png", "rb") as arq:
        dados_arquivo = arq.read()

    sleep(30)

    s.send(dados_arquivo)

    sleep(30)

    s.recv(TAMANHO_MAX_MENSAGEM)

    sleep(10)

    s.send("DISCONNECT".encode(FORMATO))
    s.recv(TAMANHO_MAX_MENSAGEM)

    resposta = jsonify({"resultado": "ok", "detalhes": "Arquivo Compartilhado na Rede!"})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta


@app_servidor_web.route("/recuperar_mensagem/<int:chave>")
def recuperar_mensagem(chave):
    chave = int(chave)

    p = Pipeline()
    p.add_pipe(recuperar, (f"{DIRETORIO_UPLOAD}/imagem.png", f"{DIRETORIO_UPLOAD}/texto_criptografado.txt"))
    p.add_pipe(descriptografar, (f"{DIRETORIO_UPLOAD}/texto_criptografado.txt", f"{DIRETORIO_UPLOAD}/mensagem.txt", chave))

    p.process()

    resposta = jsonify({"resultado": "ok", "detalhes": f"{DIRETORIO_UPLOAD}/mensagem.txt"})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta



@app_servidor_web.route("/upload_gerar", methods=['POST'])
def realizar_upload_gerar():
    
    # Apagar arquivos pré-existentes na pasta Tmp
    arquivos = [f for f in listdir(DIRETORIO_UPLOAD) if isfile(join(DIRETORIO_UPLOAD, f))]

    if arquivos != []:
        for f in arquivos:
            remove(join(DIRETORIO_UPLOAD, f))

    if 'imagem' not in request.files or 'texto' not in request.files:
        resposta = jsonify({"resultado": "erro", "detalhes": "Falta Arquivos!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    
    imagem = request.files['imagem']

    if imagem and validar_formato_imagem(imagem.filename):
        formato = secure_filename(imagem.filename).split(".")[1]
        imagem.save(join(app_servidor_web.config['DIRETORIO_UPLOAD'], f"imagem.{formato}"))

    else:
        resposta = jsonify({"resultado": "erro", "detalhes": "Formato de Imagem Inválido!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta

    texto = request.files['texto']

    if texto and validar_formato_texto(texto.filename):
        texto.save(join(app_servidor_web.config['DIRETORIO_UPLOAD'], "texto.txt"))

    else:
        resposta = jsonify({"resultado": "erro", "detalhes": "Formato de Texto Inválido!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta

    resposta = jsonify({"resultado": "ok", "detalhes": "Upload de arquivos para o servidor web finalizado"})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta


@app_servidor_web.route("/upload_recuperar", methods=['POST'])
def realizar_upload_recuperar():
    
    # Apagar arquivos pré-existentes na pasta Tmp
    arquivos = [f for f in listdir(DIRETORIO_UPLOAD) if isfile(join(DIRETORIO_UPLOAD, f))]

    if arquivos != []:
        for f in arquivos:
            remove(join(DIRETORIO_UPLOAD, f))

    if 'imagem' not in request.files:
        resposta = jsonify({"resultado": "erro", "detalhes": "Falta Arquivos!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    
    imagem = request.files['imagem']

    if imagem and validar_formato_imagem(imagem.filename):
        formato = secure_filename(imagem.filename).split(".")[1]
        imagem.save(join(app_servidor_web.config['DIRETORIO_UPLOAD'], f"imagem.{formato}"))

    else:
        resposta = jsonify({"resultado": "erro", "detalhes": "Formato de Imagem Inválido!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta

    resposta = jsonify({"resultado": "ok", "detalhes": "Upload de imagem para o servidor web finalizado"})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta


@app_servidor_web.route('/download/<string:file>')
def download(file):
    requisicao = requests.get(f"http://{ENDERECO_SERVIDOR_META}/getServerIP",headers={})
    
    if requisicao.status_code != 200:
        resposta = jsonify({"resultado": "erro", "detalhes": "Impossível contactar servidor de metadados!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    
    end_serv_arq = requisicao.json()["SERVER_IP"]
    
    if end_serv_arq == "0":
        resposta = jsonify({"resultado": "erro", "detalhes": "Servidor de arquivos inoperante!"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((end_serv_arq, PORTA_SERVIDOR_ARQUIVOS))

    s.send(f"DOWNLOAD${file}".encode(FORMATO))
    resposta = s.recv(TAMANHO_MAX_MENSAGEM).decode(FORMATO)

    if resposta.split("$")[0] == "RECEIVE_FILE":
        dados_arquivo = s.recv(TAMANHO_MAX_IMAGEM)
        with open(f"/home/{getlogin()}/Downloads/{file}", "wb") as file:
            file.write(dados_arquivo)

    else:
        resposta = jsonify({"resultado": "erro", "detalhes": "Não foi possível baixar o arquivo"})
        resposta.headers.add("Access-Control-Allow-Origin", "*")
        s.send("DISCONNECT".encode(FORMATO))
        s.recv(TAMANHO_MAX_MENSAGEM)
        return resposta
    
    s.send("OK".encode(FORMATO))
    s.send("DISCONNECT".encode(FORMATO))
    s.recv(TAMANHO_MAX_MENSAGEM)

    resposta = jsonify({"resultado": "ok", "detalhes": "sucesso"})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta

def validar_formato_imagem(img):
    return '.' in img and img.rsplit('.', 1)[1].lower() in EXT_IMAGENS

def validar_formato_texto(texto):
    return '.' in texto and texto.rsplit('.', 1)[1].lower() in EXT_TEXTO

app_servidor_web.run(port=PORTA_SERVIDOR_WEB)