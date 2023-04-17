import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

import re

nltk.download('punkt')

# Carregar os dados do arquivo JSON
with open('_locais.json', encoding='utf-8') as f:
    data = json.load(f)

# Inicializar o analisador de sentimentos
sia = SentimentIntensityAnalyzer()

# Carregar o arquivo com as novas pontuações
with open('_scores.json', encoding='utf-8') as f:
    new_scores = json.load(f)

# Atualizar o objeto sia.lexicon com as novas pontuações
sia.lexicon.update(new_scores)

# Definir um filtro de idioma para as stopwords em português
stopwords_pt = set(stopwords.words('portuguese'))

# Definindo a entrada do usuário
feedback = input("Digite uma palavra ou frase relacionada à sua preferência de restaurante: ")

# Realizando análise de sentimentos da entrada do usuário
sentimento = sia.polarity_scores(feedback)['compound']

# Transformar a entrada do usuário em uma expressão regular para pesquisa de frase completa
feedback_regex = re.escape(feedback)


# Recomendação de restaurantes
recomendados = []
for restaurante in data:
    # Análise de sentimento das avaliações que contêm a frase digitada pelo usuário
    avaliacoes = restaurante["reviews"]
    sentimento_avaliacoes = [sia.polarity_scores(review["content"])["compound"] for review in avaliacoes if re.search(feedback_regex, review["content"].lower())]
    if sentimento_avaliacoes:
        # Se houver pelo menos uma avaliação com a frase digitada, calcular a média de sentimentos
        media_sentimento = sum(sentimento_avaliacoes) / len(sentimento_avaliacoes)
        # Adicionar o restaurante à lista de recomendados com base na média de sentimentos
        recomendados.append((restaurante, media_sentimento))

# Classificando a lista de restaurantes recomendados com base na média de sentimentos
if recomendados:
    # Classificando os restaurantes de acordo com o sentimento da entrada do usuário
    if sentimento > 0:
        # Para entradas positivas, classificar em ordem decrescente de média de sentimentos
        recomendados = sorted(recomendados, key=lambda r: r[1], reverse=True)
    elif sentimento < 0:
        # Para entradas negativas, classificar em ordem crescente de média de sentimentos
        recomendados = sorted(recomendados, key=lambda r: r[1])
    else:
        # Para entradas neutras, não classificar
        pass
    # Apresentando os top 10 restaurantes recomendados
    print("Recomendamos os seguintes restaurantes:")
    for restaurante, media_sentimento in recomendados[:10]:
        print(restaurante["name"] + " - Média de sentimento: " + str(media_sentimento) + "\n- Avaliação: " + restaurante["average_rating"] + "\n- Endereço: " + restaurante["address"] + "\n")
else:
    print("Não encontramos nenhum restaurante que atenda às suas preferências.")
