# Importando Bibliotecas

import fdb
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import os
import requests
import time


#Selecionando arquivo do banco de dados

def select_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo database.fdb",
        filetypes=[("Firebird database files", "*.fdb")]
    )

    return file_path

file_path = select_file()


# Conectando com o banco Firebird

con = fdb.connect(
    dsn=file_path,
    user='SYSDBA',
    password='masterkey'
    # charset='UTF8'
)

cur = con.cursor() # Cria objeto usado para realizar operações em um banco de dados


# Integração das tabelas

cur.execute("SELECT BAIRRO, CEP, CIDADE, COMPLEMENTO, CONTATO, EMAIL, ENDERECO, IE_RG, IM, FANTASIA, CNPJ_CNPF, TELEFONE, CELULAR, UF FROM CLIENTE") # Conectando com o banco de dados a ser migrado
rows = cur.fetchall()
print(rows)

dados_payload = []
mensagens = []
dfErros = []

# lendo tabela Unidade OrganizePDV

dados_payload = []

url = "http://127.0.0.1:8090/api/ControllerPessoa?pagesize=9999999&page=1"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

for row in rows:

    payload = {
        "CBAIRRO": row[0], 
        "CCEP": row[1],
        "CCIDADE": row[2],
        "CCNAE": row[0], ###
        "CCOMP": row[3],
        "CCONTATO": row[4],
        "CEMAIL": row[5],
        "CEND": row[6],
        "CIE": row[7],
        "CIM": row[8],
        "CNOMEFAN": row[9],
        "CRAZAO": row[0], ###
        "CRF": row[10], # CNPJ?
        "CTEL1": row[11],
        "CTEL2": row[12],
        "UF": row[13],
}
    dados_payload.append(payload)


print(dados_payload)
exit(0)

for payload in dados_payload:
    url = "http://127.0.0.1:8090/api/ControllerPessoa" # Conectando com o PDV
    response = requests.post(url, json=payload)

    print(response.status_code)
    print(response.json()["detailedMessage"])
    print(response.json()["data"]["CCDVE"])


'''
SELECT CODIGO, NOME, FANTASIA, CONTATO, CNPJ_CNPF, IE_RG, IM, ENDERECO, NUMERO, COMPLEMENTO, BAIRRO, CIDADE, ID_MUNICIPIO, UF, CEP, COB_ENDERECO, COB_NUMERO, COB_COMPLEMENTO, COB_BAIRRO, COB_CIDADE, COB_UF, COB_CEP, 
TELEFONE, CELULAR, FAX, EMAIL, RENDA, LIMITE_CREDITO, DIA_DE_ACERTO, VALOR_A_RECEBER, VALOR_EM_ATRASO, CADASTRO, ULTIMA_VENDA, REG_SIMPLES, OBSERVACOES, PARCELAS_ATRA, CONVENIO, NASCIMENTO, EST_CIVIL, PAI, MAE, NATURALIDADE, 
LOCTRA, "LOCAL", PAIS_BACEN, PAIS_NOME, SITUACAO, PROFISSAO, PERSONAL1, PERSONAL2, PERSONAL3, PERSONAL4, PERSONAL5, PERSONAL6, FOTO, CONJUGE, SEXO, CONSUMIDOR, ORGAO_PUBLICO, INDIEDEST, SUFRAMA, PRAZO_CARENCIA, ID_TABELAPRECO, 
COB_EMAIL, ID_OPERADOR, ID_VENDEDOR
FROM CLIENTE;
'''