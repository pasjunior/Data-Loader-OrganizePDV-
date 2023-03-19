# Data Loader
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/pasjunior/Data-Loader-OrganizePDV-/tree/main)

# Descrição do projeto
Este código tem como objetivo integrar tabelas do banco de dados Firebird com as tabelas do sistema OrganizePDV por meio da API RESTful.

## Bibliotecas utilizadas

* fdb: biblioteca utilizada para a conexão com o banco de dados Firebird.
* tkinter: biblioteca utilizada para criação de interfaces gráficas.
* filedialog: classe da biblioteca tkinter que permite ao usuário selecionar um arquivo através de uma janela de diálogo.
* messagebox: classe da biblioteca tkinter que exibe uma mensagem em uma janela de diálogo.
* pandas: biblioteca utilizada para manipulação e análise de dados.
* numpy: biblioteca utilizada para cálculos em matrizes e vetores.
* os: biblioteca utilizada para manipulação de arquivos e pastas do sistema operacional.
* requests: biblioteca utilizada para realizar requisições HTTP.
* time: biblioteca utilizada para realizar a pausa na execução do programa.

## Seleção do arquivo do banco de dados
A função select_file() é responsável por exibir uma janela de diálogo para que o usuário selecione o arquivo database.fdb.

## Conexão com o banco de dados Firebird
A função con = fdb.connect(dsn=file_path, user='SYSDBA', password='masterkey') realiza a conexão com o banco de dados Firebird utilizando os dados de usuário e senha padrão.

## Verificação de arquivo existente
Antes de iniciar a integração de dados, o código verifica se o arquivo dePara_unidade_Gdoor.xlsx existe, se o arquivo não existir, ele cria um novo arquivo com uma planilha chamada UNIDADE, se o arquivo existir, ele lê o arquivo e carrega os dados em um DataFrame.

## Verificação de divergências
O código faz um select na tabela ESTOQUE do banco de dados para as colunas UND e UND_COMPRA e verifica se existem divergências entre as unidades do banco de dados e as unidades presentes no arquivo dePara_unidade_Gdoor.xlsx. Caso existam divergências, as unidades ausentes no arquivo são adicionadas em uma nova linha do DataFrame dePara e o arquivo é atualizado.

# Integração das tabelas
Por fim, o código realiza a integração dos dados do banco de dados Firebird com as tabelas do sistema OrganizePDV por meio da API RESTful. Ele lê as tabelas Unidade e NCM do sistema OrganizePDV, itera sobre as linhas do banco de dados, cria um payload com as informações necessárias e faz uma requisição HTTP para a API RESTful. Caso ocorra algum erro durante o processo, o código exibe uma mensagem de erro e salva os registros em um DataFrame chamado dfErros.

# Contribuições
Contribuições para o projeto são sempre bem-vindas! Caso você queira sugerir melhorias, correções de bugs ou novas funcionalidades, por favor, abra uma issue ou pull request.
