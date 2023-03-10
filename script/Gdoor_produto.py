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


# Faz um select na tabela selecionada do banco de dados para UND_VENDA

cur.execute("SELECT DISTINCT UND FROM ESTOQUE")

rows = cur.fetchall()
print(rows)


# Verificar se o arquivo 'dePara_unidade_Gdoor.xlsx' existe

if not os.path.exists('dePara_unidade_Gdoor.xlsx'):
    # Se o arquivo não existir, criar um novo arquivo com uma planilha 'UNIDADE'
    dePara = pd.DataFrame({'de': [], 'para': []})
    writer = pd.ExcelWriter('dePara_unidade_Gdoor.xlsx', engine='xlsxwriter')
    dePara.to_excel(writer, sheet_name='UNIDADE', index=False)
    writer.save()
else:
    # Se o arquivo existir, ler o arquivo e carregar os dados em um DataFrame
    dePara = pd.read_excel('dePara_unidade_Gdoor.xlsx', sheet_name='UNIDADE')

dePara = pd.DataFrame(dePara)
print(dePara)


# Imprime as divergências

divergencia = []

for row in rows:
    unidade = 'EM BRANCO' if row[0] is None else row[0]
    if not dePara['de'].isin([unidade]).any():
        divergencia.append(f"unidade '{unidade}' não existe")


print(divergencia)

# Imprime os registros na coluna 'de'

for row in divergencia:
    unidade = row.split("'")[1]
    dePara = pd.concat([dePara, pd.DataFrame(
        {'de': [unidade], 'para': [None]})], ignore_index=True)


# Escreve no arquivo excel

dePara.to_excel('dePara_unidade_Gdoor.xlsx', sheet_name='UNIDADE', index=False)


# Procura se existe registros em branco

dePara_null = dePara[dePara.isnull().any(axis=1)]
if dePara_null.empty:
    print('Não há linhas sem preenchimento.')
else:
    messagebox.showinfo("Informação", 'As seguintes linhas estão sem preenchimento:\n' + dePara_null.to_string(index=False))
    exit(0)


# Faz um select na tabela selecionada do banco de dados para UND_COMPRA

cur.execute("SELECT DISTINCT UND_COMPRA FROM ESTOQUE")

rows = cur.fetchall()
print(rows)

dePara = pd.read_excel('dePara_unidade_Gdoor.xlsx', sheet_name='UNIDADE')

dePara = pd.DataFrame(dePara)
print(dePara)


# Imprime as divergências

divergencia = []

for row in rows:
    unidade = 'EM BRANCO' if row[0] is None else row[0]
    if not dePara['de'].isin([unidade]).any():
        divergencia.append(f"unidade '{unidade}' não existe")

print(divergencia)


# Imprime os registros na coluna 'de'

for row in divergencia:
    unidade = row.split("'")[1]
    dePara = pd.concat([dePara, pd.DataFrame(
        {'de': [unidade], 'para': [None]})], ignore_index=True)


# Escreve no arquivo excel

dePara.to_excel('dePara_unidade_Gdoor.xlsx',sheet_name='UNIDADE', index=False)


# Procura se existe registros em branco

dePara_null = dePara[dePara.isnull().any(axis=1)]
if dePara_null.empty:
    print('Não há linhas sem preenchimento.')
else:
    messagebox.showinfo("Informação", 'As seguintes linhas estão sem preenchimento:\n' + dePara_null.to_string(index=False))
    exit(0)


# Integração das tabelas

cur.execute("SELECT CODIGO, BARRAS, DESCRICAO, UND, UND_COMPRA, COD_CEST, COD_NCM, TIPO_ITEM, FOTO, PESO, OBSERVACOES FROM ESTOQUE") # Conectando com o banco de dados a ser migrado
rows = cur.fetchall()

dados_payload = []
mensagens = []
dfErros = []


# lendo tabela Unidade OrganizePDV

url = f"http://127.0.0.1:8090/api/ControllerUnidade?pagesize=9999999999&page=1"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

respostaJson_unidade = response.json()
itemsJson_unidade = respostaJson_unidade['items']


# lendo tabela NCM OrganizePDV

url = f"http://127.0.0.1:8090/api/ControllerNCM?pagesize=9999999999&page=1"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

respostaJson_ncm = response.json()
itemsJson_ncm = respostaJson_ncm['items']
    

for row in rows:
# UND_VENDA
    und_venda = 'EM BRANCO' if row[3] is None else row[3]
    if (dePara['de'] == und_venda).any():
        sigla_und_venda = dePara.loc[dePara['de'] == und_venda, 'para'].iloc[0]
    else:
        dfErros.append({'codigo': row[0], 'descrição': row[2], 'divergencia': f'Unidade de venda {und_venda} não existe no dePara'})
        continue
    
    unidade_venda = {}
    for unidade in itemsJson_unidade:
        if unidade["CSIGLA"] == sigla_und_venda:
            unidade_venda = unidade
    if not unidade_venda:
        dfErros.append({'codigo': row[0], 'descrição': row[2], 'divergencia': f'Unidade de venda {sigla_und_venda} não existe no PDV'})
        continue

# UND_COMPRA
    und_compra = 'EM BRANCO' if row[4] is None else row[4]

    if (dePara['de'] == und_compra).any():
        sigla_und_compra = dePara.loc[dePara['de'] == und_compra, 'para'].iloc[0]
    else: 
        dfErros.append({'codigo': row[0], 'descrição': row[2], 'divergencia': f'Unidade de Compra {und_compra} não existe no dePara'})
        continue

    unidade_compra = {}
    for unidade in itemsJson_unidade:
        if unidade["CSIGLA"] == sigla_und_compra:
            unidade_compra = unidade
    if not unidade_compra:
        dfErros.append({'codigo': row[0], 'descrição': row[2], 'divergencia': f'Unidade de Compra {sigla_und_compra} não existe no PDV'})
        continue

# NCM
    cod_ncm = row[6]
    ncm = {}
    for ncmpdv in itemsJson_ncm:
        if ncmpdv["CNCM"] == cod_ncm:
            ncm = ncmpdv
    if not ncm:
        dfErros.append({'codigo': row[0], 'descrição': row[2], 'divergencia': f'Código NCM {cod_ncm} não existe no PDV'})
        continue
    
    payload = {
        #"CCDVE": row[0],
        "CCODBAR": row[1], #OK
        "CDESCRICAO": row[2], #OK
        "O1UM-NID": unidade_venda['NID'], #OK
        "O2UM-NID": unidade_compra['NID'], #OK
        "ONCM-NID": ncm['NID'],
        "CTIPO": row[7], #OK
        "OTE-NID": 1,
        "OTS-NID": 2,
        "NPLIQ": float(row[9]), # Tive que converter em float pq a biblioteca requests n reconhece números decimais
        "NPBRU": float(row[9])
}
  

    dados_payload.append(payload)
       

if len(dfErros) > 0:
    dfErros = pd.DataFrame(dfErros)
    dfErros.to_excel('erros_Gdoor.xlsx', sheet_name='ERROS', index=False)
    messagebox.showinfo("Atenção", f'Tratar os erros em: erros_Gdoor.xlsx')
    
print(dados_payload)
exit(0)

for payload in dados_payload:
    url = "http://127.0.0.1:8090/api/ControllerProduto" # Conectando com o PDV
    response = requests.post(url, json=payload)

    print(response.status_code)
    print(response.json()["detailedMessage"])
    print(response.json()["data"]["CCDVE"])