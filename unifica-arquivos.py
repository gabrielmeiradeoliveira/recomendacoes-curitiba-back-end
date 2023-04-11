import json

try:
    # Carregando os arquivos JSON em objetos separados
    with open('locais_pag_25_30.json') as f:
        json_obj1 = json.load(f)

    with open('locais_pag_31_34.json') as f:
        json_obj2 = json.load(f)

    # Criando um novo objeto vazio para armazenar a combinação dos dois objetos JSON
    combined_json_obj = {}

    # Adicionando cada chave-valor do json_obj1 ao combined_json_obj
    for key, value in json_obj1.items():
        combined_json_obj[key] = value

    # Adicionando cada chave-valor do json_obj2 ao combined_json_obj
    for key, value in json_obj2.items():
        combined_json_obj[key] = value

    # Salvando o combined_json_obj em um arquivo JSON
    with open('arquivo_combinado.json', 'w') as f:
        json.dump(combined_json_obj, f)

except FileNotFoundError:
    print('Um ou mais arquivos não foram encontrados.')
except json.JSONDecodeError:
    print('Um ou mais arquivos contêm dados JSON inválidos.')
