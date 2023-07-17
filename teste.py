import os
import pandas as pd


filename = '\\\\dmsrv-nfs/Temporario/Correios/planilha_correios_tecnopharma/'
arquivos = os.listdir(filename)
arquivo_xlsx = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]
arquivo_xlsx = arquivo_xlsx[0]
caminho_arquivo = os.path.join(filename, arquivo_xlsx)
df = pd.read_csv(caminho_arquivo, sep=';', skiprows=2, encoding='cp1252')
print('Aqui DF',df['Etiqueta'])