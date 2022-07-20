from flask import *
from config import PORTA_SERVIDOR_META

SERVER_IP = "0"

app_servidor_meta = Flask(__name__)

@app_servidor_meta.route("/")
def inicio():
    return "Servidor de Metadados ativo!"

@app_servidor_meta.route("/getServerIP")
def get_server_ip():
    resposta = jsonify({"SERVER_IP": SERVER_IP})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    
    return resposta

@app_servidor_meta.route("/setServerIP/<string:ip>")
def set_server_ip(ip):
    global SERVER_IP
    SERVER_IP = ip    
    
    resposta = jsonify({"SERVER_IP": SERVER_IP})
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    
    return resposta

app_servidor_meta.run(port=PORTA_SERVIDOR_META)