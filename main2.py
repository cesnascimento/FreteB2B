import pandas as pd
import re
from headers_vipp import headers_vipp

import re


def limpar_string(string):
  if 'R$' in string:
    string = re.sub(r'R\$', '', string)
  if ',' in string: 
    string = re.sub(r',', '.', string)

  return float(string)


def abrir_planilha():
  dicionario = dict()
  filename = 'planilhas/fatura-668065.csv'
  df = pd.read_csv(filename, skiprows=6, sep=';', encoding='cp1252')
  numeros_rastreios = df['Numero da Etiqueta'].dropna().tolist()
  valores_unitarios = df['Valor Unitario (R$)'].dropna().tolist()
  for num, val in zip(numeros_rastreios, valores_unitarios):
    dicionario[num] = limpar_string(val)
  return dicionario


def dados_vipp(rastreio):
  dicionario = dict()
  dados = headers_vipp(rastreio)
  for dado in dados.values():
    print(dado[0])
    dicionario[int(dado[0])] = dado[1]
  return dicionario



def abrir_planilha_distriprime():
  dicionario = dict()
  filename = 'planilhas/correiosdistri.csv'
  df = pd.read_csv(filename, sep=';', encoding='cp1252')
  notas_fiscais = df['Nota fiscal'].dropna().tolist()
  valores_frete = df['Valor frete'].dropna().tolist()
  for num, val in zip(notas_fiscais, valores_frete):
    dicionario[num] =  limpar_string(val)
  return dicionario


def comparar(dados1, dados2):
  for chave, valor in dados1.items():
    if chave in dados2:
        if dados2[chave] == valor:
            status = "presente"
        else:
            status = "presente, mas com valor diferente"
    else:
        status = "ausente"
    print(f"A chave '{chave}' com valor '{valor}' está {status} em Dicionário A.")

  # Verificar chaves do Dicionário B ausentes em Dicionário A
  chaves_ausentes = [chave for chave in dados1 if chave not in dados2]
  for chave in chaves_ausentes:
      valor = dados1[chave]
      print(f"A chave '{chave}' com valor '{valor}' não está presente em Dicionário A.")




if __name__ == '__main__':
  dados_correios = abrir_planilha()
  dados_distriprime = abrir_planilha_distriprime()
  for key, val in dados_correios.items():
    info_vipp = dados_vipp(key)
    info = comparar(info_vipp, dados_distriprime)
    
