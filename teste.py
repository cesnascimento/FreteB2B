import pandas as pd
import re
from headers_vipp_tec import headers_vipp
import re
import os


def limpar_string(string):
    if 'R$' in string:
        string = re.sub(r'R\$', '', string)
    if ',' in string:
        string = re.sub(r',', '.', string)

    return float(string)


def abrir_planilha():
    dicionario = dict()
    filename = '\\\\dmsrv-nfs/Temporario/Correios/planilha_correios_tecnopharma/'
    arquivos = os.listdir(filename)
    arquivo_xlsx = [arquivo for arquivo in arquivos if arquivo.endswith('.xlsx')]
    arquivo_xlsx = arquivo_xlsx[0]
    caminho_arquivo = os.path.join(filename, arquivo_xlsx)
    df = pd.read_excel(caminho_arquivo, skiprows=2)
    print(df.columns)
    numeros_rastreios = df['Etiqueta'].dropna().tolist()
    valores_unitarios = df['COBRADO'].dropna().tolist()
    for num, val in zip(numeros_rastreios, valores_unitarios):
        dicionario[num] = limpar_string(str(val))
    return dicionario


def dados_vipp(rastreio):
    dicionario = dict()
    dados = headers_vipp(rastreio)
    for key, val in dados.items():
        try:
            dicionario[int(val[0])] = [val[1], val[2], key, val[3]]
        except Exception as e:
            print('DEU ERRO', e)
    print(dicionario)
    return dicionario


def abrir_planilha_distriprime():
    dicionario = dict()
    filename = '\\\\dmsrv-nfs/Temporario/Correios/correiostec.csv'
    if os.path.exists(filename):
      print("O diretório existe.")
    else:
      print("O diretório não existe.")
    df = pd.read_csv(filename, sep=';', encoding='cp1252')
    notas_fiscais = df['Nota fiscal'].dropna().tolist()
    valores_frete = df['Valor frete'].dropna().tolist()
    for num, val in zip(notas_fiscais, valores_frete):
        dicionario[num] = limpar_string(val)
    return dicionario



def comparar(dados_vipp, dados_distriprime):
    resultados = []
    for chave, valor in dados_vipp.items():
        print('VIPP VALOR',valor)
        if chave in dados_distriprime:
            if dados_distriprime[chave] == valor[0]:
                status = "presente"
                valor_distriprime = dados_distriprime[chave]
                cliente = valor[1]
                resultados.append({
                    'Data': valor[3],
                    'Cliente': cliente,
                    'Codigo Rastreio': valor[2],
                    'Nota Fiscal': chave,
                    'Valor Correios': valor[0],
                    'Status': status,
                    'Valor Dermage': valor_distriprime
                })
            else:
                status = "presente, mas com valor diferente"
                valor_distriprime = dados_distriprime[chave]
                cliente = valor[1]
                resultados.append({
                    'Data': valor[3],
                    'Cliente': cliente,
                    'Codigo Rastreio': valor[2],
                    'Nota Fiscal': chave,
                    'Valor Correios': valor[0],
                    'Status': status,
                    'Valor Dermage': valor_distriprime,
                    'Diferença': abs(valor[0] - valor_distriprime)
                })
        else:
            status = "ausente"
            resultados.append({
                'Codigo Rastreio': valor[2],
                'Nota Fiscal': chave,
                'Valor Correios': valor[0],
                'Status': status,
                'Valor Dermage': None
            })

    chaves_ausentes = [chave for chave in dados_vipp if chave not in dados_distriprime]
    for chave in chaves_ausentes:
        valor = dados_vipp[chave]
        print(f"A chave '{chave}' com valor '{valor}' não está presente em dados_distriprime.")

    return pd.DataFrame(resultados)


if __name__ == '__main__':
    dados_correios = abrir_planilha()
    dados_distriprime = abrir_planilha_distriprime()
    dataframes = []
    for key, val in dados_correios.items():
        print(key, val)
        try:
            info_vipp = comparar(dados_vipp(key), dados_distriprime)
            dataframes.append(info_vipp)
        except IndexError as e:
            print(e, key, val)
            pass