import requests

url = 'http://localhost:5000/recomendar'

feedback = 'O serviço é horrível e a comida é ruim'

payload = {'feedback': feedback}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(data['message'])
    for restaurante in data['restaurantes']:
        print(restaurante['nome'], restaurante['media_sentimento'], restaurante['avaliacao'], restaurante['endereco'])
else:
    print('Erro ao obter recomendações:', response.status_code)