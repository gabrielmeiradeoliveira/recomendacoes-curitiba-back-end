from flask import Flask, request, jsonify
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

nltk.download('punkt')

# Carregar os dados do arquivo JSON
try:
    with open('_locais.json', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print("Erro ao carregar o arquivo '_locais.json':", e)
    data = []

# Inicializar o analisador de sentimentos
sia = SentimentIntensityAnalyzer()

# Carregar o arquivo com as novas pontuações
try:
    with open('_scores.json', encoding='utf-8') as f:
        new_scores = json.load(f)
    # Atualizar o objeto sia.lexicon com as novas pontuações
    sia.lexicon.update(new_scores)
except Exception as e:
    print("Erro ao carregar o arquivo '_scores.json':", e)

# Definir um filtro de idioma para as stopwords em português
stopwords_pt = set(stopwords.words('portuguese'))

app = Flask(__name__)

@app.route('/recomendar', methods=['POST'])
def recomendar():
    # Receber a entrada do usuário em formato de JSON
    feedback = request.get_json()['feedback']
    
    # Realizando análise de sentimentos da entrada do usuário
    sentimento = sia.polarity_scores(feedback)['compound']

    # Recomendação de restaurantes
    recomendados = []
    for restaurante in data:
        # Análise de sentimento das avaliações que contêm a palavra ou frase digitada pelo usuário
        avaliacoes = restaurante["reviews"]
        sentimento_avaliacoes = [sia.polarity_scores(review["content"])["compound"] for review in avaliacoes if feedback in review["content"].lower() or any(palavra in review["content"].lower() for palavra in feedback.split())]
        if sentimento_avaliacoes:
            # Se houver pelo menos uma avaliação com a palavra ou frase digitada, calcular a média de sentimentos
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
        # Retornando os top 10 restaurantes recomendados
        return {"message": "Recomendamos os seguintes restaurantes:", "restaurantes": [{"nome": restaurante["name"], "media_sentimento": media_sentimento, "avaliacao": restaurante["average_rating"], "endereco": restaurante["address"]} for restaurante, media_sentimento in recomendados[:10]]}
    else:
        return {"message": "Não encontramos nenhum restaurante que atenda às suas preferências. " }
    
if __name__ == '__main__':
    app.run()