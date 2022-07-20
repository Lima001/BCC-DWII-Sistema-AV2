import cv2
import numpy as np

def toBin(dado):
    if type(dado) == str:
        return ''.join([ format(ord(i), "08b") for i in dado ])
    elif type(dado) == bytes or type(dado) == np.ndarray:
        return [ format(i, "08b") for i in dado ]
    elif type(dado) == int or type(dado) == np.uint8:
        return format(dado, "08b")
    else:
        raise TypeError("Tipo de dado não suportado...")

def esteganografar(imagem_entrada, imagem_saida, arquivo_dados):
    imagem = cv2.imread(imagem_entrada) 
    n_bytes = imagem.shape[0] * imagem.shape[1] // 8

    arq_dados = open(arquivo_dados, "r")
    dados = "".join([i for i in arq_dados.readlines()]) + "#####"
    arq_dados.close()
    
    dados_binario = toBin(dados)
    tamanho = len(dados_binario)
    index = 0

    for values in imagem:
        for pixel in values:
            
            g = toBin(pixel[1])

            if index < tamanho:
                pixel[1] = int(g[:-1] + dados_binario[index], 2)
                index += 1
    
            if index >= tamanho:
                break

    cv2.imwrite(f"{imagem_saida}.png", imagem)

def recuperar(imagem, dados_saida):
    imagem = cv2.imread(imagem)
    
    dados_bin = ""

    for values in imagem:
        for pixel in values:
            g = toBin(pixel[1])
            dados_bin += g[-1]

    all_bytes = [ dados_bin[i: i+8] for i in range(0, len(dados_bin), 8) ]

    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####":
            break
    
    arq_dados = open(dados_saida,"w")
    arq_dados.write(decoded_data[:-5])
    arq_dados.close()

if __name__ == "__main__":
    esteganografar("base.jpeg","saida","source.txt")
    recuperar("saida.png","output.txt")