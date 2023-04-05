import json
from textblob import TextBlob

# Carregando o JSON em uma variável
with open("restaurante_meu.json", encoding='utf-8') as f:
    dados = json.load(f)

# Definindo a frase ou palavra do usuário
feedback = input("Digite uma palavra ou frase relacionada à sua preferência de restaurante: ")

# Realizando análise de sentimentos
sentimento = TextBlob(feedback).sentiment.polarity
if sentimento > 0:
    print("O feedback do usuário é positivo.")
elif sentimento == 0:
    print("O feedback do usuário é neutro.")
else:
    print("O feedback do usuário é negativo.")

# Recomendação de restaurantes
recomendados = []
for restaurante in dados:
    for review in restaurante["reviews"]:
        if any(palavra in review["content"].lower() for palavra in feedback.split()):
            recomendados.append(restaurante)
            break

# Apresentando a recomendação
if recomendados:
    print("Recomendamos os seguintes restaurantes:")
    for restaurante in recomendados:
        print(restaurante["name"] + " - Avaliação: " + restaurante["average_rating"] + "\n- Endereço: " + restaurante["address"] + "\n")
else:
    print("Não encontramos nenhum restaurante que atenda às suas preferências.")
