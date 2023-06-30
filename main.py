import pandas as pd


def primeira_planilha():

    dados = dict()
    # Abra a planilha e leia os dados
    df_planilha = pd.read_excel('planilhas/PLANILHA CORREIOS ATUALIZADO 17 04 23 A 16 05 23.xlsx')

    valores_coluna_5 = df_planilha.iloc[:, 5].fillna('-').tolist()[1:]
    valores_coluna_7 = df_planilha.iloc[:, 7].fillna('-').tolist()[1:]

    # Imprima os valores da coluna
    for valor5, valor7 in zip(valores_coluna_5[1:], valores_coluna_7[1:]):
        print(valor5, valor7)
        dados[valor5] = valor7
    
    return dados


def segunda_planilha():
    dados = dict()
    # Abra a planilha e leia os dados
    df_csv = pd.read_csv('planilhas/correiostec.csv', sep=';')
    num_colunas = df_csv.shape
    print("TEC Número de colunas:", num_colunas)

    valores_coluna_1 = df_csv.iloc[:, 1].fillna('-').tolist()[0:]
    valores_coluna_2 = df_csv.iloc[:, 2].fillna('-').tolist()[0:]

    for valor1, valor2 in zip(valores_coluna_1, valores_coluna_2):
        print(valor1, valor2)
        dados[valor1] = valor2
    
    return dados


def terceira_planilha():
    dados = dict()
    # Abra a planilha e leia os dados
    df_csv = pd.read_csv('planilhas/correiosdistri.csv', sep=';')
    num_colunas = df_csv.shape
    print("DISTRI Número de colunas:", num_colunas)

    valores_coluna_1 = df_csv.iloc[:, 1].fillna('-').tolist()[0:]
    valores_coluna_2 = df_csv.iloc[:, 2].fillna('-').tolist()[0:]

    for valor1, valor2 in zip(valores_coluna_1, valores_coluna_2):
        print(valor1, valor2)
        dados[valor1] = valor2
    
    return dados


def comparar_dicionarios(dic1, dic2):
    for chave in dic1:
        if chave in dic2:
            if dic1[chave] > 0:
                print("Nota Fiscal:", chave)
                print("Valor na planilha um:", dic1[chave])
                print("Valor no planilha dois:", dic2[chave])
                print() 


if __name__ == '__main__':
    planilha_um = primeira_planilha()
    planilha_dois = segunda_planilha()
    planilha_tres = terceira_planilha()

    comparar_dicionarios(planilha_um, planilha_dois)
    comparar_dicionarios(planilha_um, planilha_tres)