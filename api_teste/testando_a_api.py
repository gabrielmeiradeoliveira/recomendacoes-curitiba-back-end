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
    
    #Nesse exemplo, estamos enviando um feedback negativo sobre um restaurante e esperamos receber uma lista de recomendações de restaurantes com base, 
    #nas avaliações que contenham a palavra "horrível" ou "ruim".

    #O resultado da requisição será impresso no console, mostrando a mensagem de recomendação e os dados dos 10 restaurantes mais recomendados.
