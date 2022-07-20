def criptografar(arquivo_entrada, arquivo_saida, chave_criptografica):
    
    f1 = open(arquivo_entrada, "r")
    f2 = open(arquivo_saida, "w")
    
    l = f1.readline()[:-1]

    while (l != ""):

        resultado = ""

        for char in l:
            if not char.isalpha():
                resultado += char
            elif char.isupper():
                resultado += chr(((ord(char) - 65) + chave_criptografica) % 26 + 65)
            else:
                resultado += chr(((ord(char) - 97) + chave_criptografica) % 26 + 97)

        f2.write(resultado[::-1]+"\n")
        
        l = f1.readline()[:-1]

    f1.close()
    f2.close()

def descriptografar(arquivo_entrada, arquivo_saida, chave_criptografica):

    f1 = open(arquivo_entrada, "r")
    f2 = open(arquivo_saida, "w")
    
    l = f1.readline()[:-1]

    while (l != ""):

        resultado = ""

        for char in l:
            if not char.isalpha():
                resultado += char
            elif char.isupper():
                resultado += chr(((ord(char) - 65) - chave_criptografica) % 26 + 65)
            else:
                resultado += chr(((ord(char) - 97) - chave_criptografica) % 26 + 97)

        f2.write(resultado[::-1]+"\n")
        
        l = f1.readline()[:-1]

    f1.close()
    f2.close()

def executar_teste():
    criptografar("source.txt", "output.txt", 2)
    descriptografar("output.txt", "decrypt.txt", 2)

if __name__ == "__main__":
    executar_teste()