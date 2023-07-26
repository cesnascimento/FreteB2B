import pandas as pd
import re
from headers_vipp_tec import headers_vipp
import re
import os
from headers_prepost import access_prepost, prepostagem_session, detalhe_objeto, cookies
from bs4 import BeautifulSoup


def limpar_string(string):
    if 'R$' in string:
        string = re.sub(r'R\$', '', string)
    if ',' in string:
        string = re.sub(r',', '.', string)

    return float(string)


def abrir_planilha():
    dicionario = dict()
    #filename = '\\\\dmsrv-nfs/Temporario/Correios/planilha_correios_tecnopharma/'
    filename = 'planilha_correios_tecnopharma/'
    arquivos = os.listdir(filename)
    arquivo_xlsx = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]
    arquivo_xlsx = arquivo_xlsx[0]
    caminho_arquivo = os.path.join(filename, arquivo_xlsx)
    df = pd.read_csv(caminho_arquivo, sep=';', skiprows=2, encoding='cp1252')
    numeros_rastreios = df['Etiqueta'].dropna().tolist()
    valores_unitarios = df['Valor do Servico'].dropna().tolist()
    for num, val in zip(numeros_rastreios, valores_unitarios):
        dicionario[num] = limpar_string(val)
    return dicionario


def dados_vipp(rastreio):
    dicionario = dict()
    dados = headers_vipp(rastreio)
    for key, val in dados.items():
        try:
            dicionario[int(val[0])] = [val[1], val[2], key, val[3]]
        except Exception as e:
            print('DEU ERRO', e)
    print('diconario vipp', dicionario)
    return dicionario


def abrir_planilha_tecnopharma():
    dicionario = dict()
    #filename = '\\\\dmsrv-nfs/Temporario/Correios/correiostec.csv'
    filename = 'planilha_fatura/correiostec.csv'
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


def remove_BR_from_key(key):
    return key.replace('BR', '')


def buscar_prepostagem(dados_correios, dados_prepostagem):
    dicionario = {}
    for chave in dados_correios:
        nova_chave = remove_BR_from_key(chave)
        if nova_chave in dados_prepostagem:
            print(f'Chave: {chave}, valorers: {dados_correios[chave]}, {dados_prepostagem[nova_chave]}')
            params = {
                'idobjeto': f'{dados_prepostagem[nova_chave]}',
            }
            pagina = prepostagem_session.get(
                'https://www.prepostagem.com.br/PrePostagem/DetalhesObjetoDash.aspx',
                params=params,
                cookies=cookies
            )
            nota_fiscal, valor_postagem, valor_data, valor_destinatario = detalhe_objeto(pagina)
            dicionario[nota_fiscal] = [limpar_string(valor_postagem), valor_data, valor_destinatario, chave]
    return dicionario


def comparar_prepostagem(dados_prepostagem, dados_tecnopharma):
    resultados = []
    for chave, valor in dados_prepostagem.items():
        """ print('PREPOSTAGEM VALOR', chave, valor) """
        if chave in dados_tecnopharma:
            if dados_tecnopharma[chave] == valor[0]:
                status = "presente"
                valor_tecnopharma = dados_tecnopharma[chave]
                cliente = valor[2]
                resultados.append({
                    'Data': valor[1],
                    'Cliente': cliente,
                    'Codigo Rastreio': valor[3],
                    'Nota Fiscal': chave,
                    'Valor Correios': valor[0],
                    'Status': status,
                    'Valor Dermage': valor_tecnopharma
                })
            else:
                status = "presente, mas com valor diferente"
                valor_tecnopharma = dados_tecnopharma[chave]
                cliente = valor[2]
                resultados.append({
                    'Data': valor[1],
                    'Cliente': cliente,
                    'Codigo Rastreio': valor[3],
                    'Nota Fiscal': chave,
                    'Valor Correios': valor[0],
                    'Status': status,
                    'Valor Dermage': valor_tecnopharma,
                    'Diferença': abs(valor[0] - valor_tecnopharma)
                })
        else:
            status = "ausente"
            resultados.append({
                'Codigo Rastreio': valor[3],
                'Nota Fiscal': chave,
                'Valor Correios': valor[0],
                'Status': status,
                'Valor Dermage': None
            })

    return pd.DataFrame(resultados)


def comparar_vipp(dados_vipp, dados_tecnopharma):
    resultados = []
    for chave, valor in dados_vipp.items():
        #print('VIPP VALOR',valor)
        if chave in dados_tecnopharma:
            if dados_tecnopharma[chave] == valor[0]:
                status = "presente"
                valor_tecnopharma = dados_tecnopharma[chave]
                cliente = valor[1]
                resultados.append({
                    'Data': valor[3],
                    'Cliente': cliente,
                    'Codigo Rastreio': valor[2],
                    'Nota Fiscal': chave,
                    'Valor Correios': valor[0],
                    'Status': status,
                    'Valor Dermage': valor_tecnopharma
                })
            else:
                status = "presente, mas com valor diferente"
                valor_tecnopharma = dados_tecnopharma[chave]
                cliente = valor[1]
                resultados.append({
                    'Data': valor[3],
                    'Cliente': cliente,
                    'Codigo Rastreio': valor[2],
                    'Nota Fiscal': chave,
                    'Valor Correios': valor[0],
                    'Status': status,
                    'Valor Dermage': valor_tecnopharma,
                    'Diferença': abs(valor[0] - valor_tecnopharma)
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

    return pd.DataFrame(resultados)


if __name__ == '__main__':
    dados_correios = abrir_planilha()
    dados_tecnopharma = abrir_planilha_tecnopharma()
    dataframes = []
    dados_prepost = access_prepost()
    dados_prepostagem = buscar_prepostagem(dados_correios, dados_prepost)
    info_prepostagem = comparar_prepostagem(dados_prepostagem, dados_tecnopharma)
    dataframes.append(info_prepostagem)
    for key, val in dados_correios.items():
        print(key, val)
        try:
            info_vipp = comparar_vipp(dados_vipp(key), dados_tecnopharma)
            dataframes.append(info_vipp)
        except:
            pass

    combined_df = pd.concat(dataframes, ignore_index=True)
    with pd.ExcelWriter("todos_resultados_tecnopharma.xlsx", engine="openpyxl") as writer:
        combined_df.to_excel(writer, sheet_name="Resultados", index=False)
