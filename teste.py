import re

def limpar_string(string):
    # Remover símbolo "R$"
    string = re.sub(r'R\$', '', string)

    # Remover vírgulas
    string = re.sub(r',', '.', string)

    return float(string)

print(type(limpar_string('2.1')))