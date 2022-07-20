# BCC-DWII-Sistema-AV2
Códigos e demais artefatos utilziados como avaliação para a disciplina de Desenvolvimento Web II do 5º Semestre do Curso de Bacharelado em Ciências da Computação

## Ideia Geral do Sistema

O sistema consiste no compartilhamento de mensagens "secretas" através de imagens esteganografadas que possuem uma mensagem
critpografada escondida. O sistema em questão permite que um usuário acesse um servidor web via páginas web para criar a sua própria mensagem (fazendo o upload de uma imagem e de um arquivo de texto contendo a mensagem normal). Tendo sido gerada a menasgem "secreta", o sistema envia ao servidor de arquivos que será responsável por distribuir com todos os clientes conectados na rede do sistema.

Quando um usuário quiser recuperar uma mensagem "secreta", ele pode fazer isso acessando o servidor web e solicitando o download de uma imagem do servidor de arquivos. Com a imagem esteganografada, o usuário é capaz de acessar a funcionalidade de decifrar a mensagem (fazendo o upload e informando a chave criptográfica). Se tudo ocorrer bem, o servidor web exibirá a mensagem que estava escondida na imagem.

### Detalhes sobre o Sistema

- A criptografia implementada consiste na cifra de César. Além disso, como um adicional todas as linhas do arquivo de texto criptografado são gravadas em ordem inversa. Isso significa dizer que além de aplicar a decodificação usando cifra de César, é necessário reverter a ordem de cada linha para obter a mensagem orignal. (Código Disponível em: ServidorWeb/BibliotecasExtras/Criptografia)

- O método de esteganografia consiste em utilizar o bit menos significativo de cada ponto verde de cada pixel da imagem. Isto significa dizer que esconde-se o texto binário sobrescrevendo o bit menos significativo da informação que representa a taxa de verde do pixel da imagem. O processo é efetuado até a mensagem ter sido escondida - logo, nem todos os pixels eventualmente são sobrescritos. (Código Disponível em: ServidorWeb/BibliotecasExtras/Esteganografia)

- Idealizou-se implementar a criptografia e esteganografia utilizando a arquitetura Pipe-and-Filters, porém não foi possível cumprir os principais ideais desse modelo. Sendo assim, implementou-se uma pseudo-arquitetura baseada em funções e filtros. (Código Disponível em: ServidorWeb/BibliotecasExtras/Pipe)

- Existe um servidor de metadados responsável por manter informações da rede de compartilhamento de arquivos. Todo "ponto" que desejar conectar-se a rede deve consultar esse servidor para saber o endereço do servidor de arquivos central.

- O servidor web é responsável por aplicar a funcionalidade de "esconder" mensagens e fazer a ligação com a rede de compartilhamento de imagens. Um usuário só tem acessos às mensagens via servidor web.

- A rede de distribuição de imagens foi imaginada como uma rede P2P, porém não foi possível implementar verdadeiramente um sistema dessa natureza. No sistema atual, cada ponto pode tornar-se um servidor de arquivos ou um cliente desse servidor, porém não ao mesmo tempo. Além disso, não foi possível implementar outros aspectos pertinentes a esse tipo de rede - como consistência e descentralização.

## Arquivos/Pastas Disponibilizados

- **ArquivosExtras:** Contém arquivos de exemplo para utilizar durante a interação do sistema

- **Front-end:** Contém as páginas HTML do sistema, bem como os códigos javascript (com jquery)

- **RedeCompartilhamentoImagens:** Códigos para executar a rede de compartilhamento de imagens

- **ServidorMetadados**: Código do servidor de metadados

- **ServidorWeb**: Código do servidor Web, bem como pastas utilizadas pelo servidor. Além disso, é nessa pasta que pode-se encontrar os programas implementados para aplicação de criptografia e esteganografia usados pelo sistema

## Como executar

Para executar, deve-se seguir os seguintes passos:

- Executar o Servidor de Metadados *servidorMeta.py*

- Executar o Servidor Web *servidorWeb.py*

- Executar o Servidor de Arquivos *p2p.py* - esse programa é responsável por verificar a existência de um servidor de arquivos ativo. Caso não exista, o servidor é criado

- Opcional: Executar N clientes do Servidor de Arquivos *p2p.py* - Existindo um servidor de arquivo, executar o porgrama em questão cria clientes que conectam-se ao servidor de arquivo.

- Interagir com o servidor web via páginas html - A página inicial chama-se *index.html*, a partir dela é possível usar o sistema

### Observações rápidas

- O login e senha para acessar o sistema são respectivamente: root e toor

- Existe uma réplica do arquivo *config.py* em praticamente todas as pastas de código (o que pretende-se mudar futuramente). Caso deseje alterar algum parâmetro do sistema, verifique e altere todos os arquivos de configuração

## Problemas Existentes

Por se tratar de um protótipo e existir um prazo de entrega para a avaliação, o sistema em questão apresenta diversos problemas que podem/devem ser resolvidos para que seu uso seja viável. Dentre os principais problemas, cita-se: Desempenho, e Confiabilidade. Por exemplo, não existe nenhuma validação se o envio/recebimento de arquivos a partir do servidor de arquivo está ocorrendo em sua totalidade - o que pode gerar (e gera) diversos erros e comportamento indeseável quando o sistema é executado em uma rede que não garanta condições ótimas de envio.

## Referências

### Livros
- FAIRBANKS, George. Just enough software architecture: a risk-driven approach. Marshall & Brainerd, 2010.
- PILLAI, Anand B. Software Architecture with Python. Packt Publishing, 2017.
- RICHARDS, Mark; FORD, Neal. Fundamentals of Software Architecture: An Engineering Approach. O'Reilly Media, 2020.
- RICHARDS, Mark. Software Architecture Patterns. O'Reilly Media, 2015.

### Sites
- KANIECKI, Kyle. Pipe & Filter Pattern in Python. 2020. Disponível em: https://kylekaniecki.com/blog/testing-pipe-filter-pattern-django/
- NAGPAL, Aman. How to create your own decentralized file sharing service using python. 2018. Disponível em: https://medium.com/@amannagpal4/how-to-create-your-own-decentralized-file-sharing-service-using-python-2e00005bdc4a
- ROY, Rupali. Image Steganography using Python. 2020. Disponível em: https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372

### Vídeos
- Multithreaded File Transfer using TCP Socket in Python | Socket Programming in Python. Disponível em: https://youtu.be/FQ-scCeKWas

## Observação Final

Pretende-se aprimorar esse código para além do escopo da avaliação da disciplina. Espera-se resolver os problemas citados anteriromente, bem como possivelmente implementar a rede de distribuição de arquivos como uma rede verdadeiramente ponto a ponto. Além disso, estuda-se a possibilidade de implementar as bibliotecas de processamento de texto e imagem seguindo o modelo de arquitetura Pipe-and-Filter.

Todavia, incialmente pretende-se adicionar uma documentação mais robusta, com comentários em cada código, e arquivos explicando o funcionamento de cada módulo do sistema de maneira simples.
