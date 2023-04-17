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

@app.route('/recomendar', methods=['GET'])
def recomendar():
    # Receber a entrada do usuário em formato de JSONP
    callback = request.args.get('callback')
    feedback = request.args.get('feedback')

    # Realizando análise de sentimentos da entrada do usuário
    sentimento = sia.polarity_scores(feedback)['compound']

    # Recomendação de restaurantes
    recomendados = []
    for restaurante in data:
        # Análise de sentimento das avaliações que contêm a palavra ou frase digitada pelo usuário
        avaliacoes = restaurante["reviews"]
        sentimento_avaliacoes = [sia.polarity_scores(review["content"])["compound"] for review in avaliacoes if all(palavra in review["content"].lower() for palavra in feedback.split())]
        if sentimento_avaliacoes:
            # Se houver pelo menos uma avaliação com a palavra ou frase digitada, calcular a média de sentimentos
            media_sentimento = sum(sentimento_avaliacoes) / len(sentimento_avaliacoes)
            # Adicionar o restaurante à lista de recomendados com base na média de sentimentos
            recomendados.append((restaurante, media_sentimento))
    
     # Classificando a lista de restaurantes recomendados com base na média de sentimentos
    if recomendados:
        media_sentimentos = sum([r[1] for r in recomendados])/len(recomendados)
        recomendados = [(r[0], r[1], sentimento - r[1]) for r in recomendados]
        recomendados = sorted(recomendados, key=lambda r: r[2])
        recomendados = [(r[0], r[1]) for r in recomendados]

    # Classificando os restaurantes de acordo com o sentimento da entrada do usuário
    if sentimento > 0:
        # Para entradas positivas, classificar em ordem decrescente de média de sentimentos
        recomendados = sorted(recomendados, key=lambda r: r[1], reverse=True)
    elif sentimento < 0:
        # Para entradas negativas, classificar em ordem crescente de média de sentimentos
        recomendados = sorted(recomendados, key=lambda r: r[1])
    else:
        # Caso o sentimento seja neutro, manter a ordem original da lista
        pass

    # Retornando os top 10 restaurantes recomendados
    top10_recomendados = recomendados[:10]

    # Criar um objeto JSON com os restaurantes recomendados
    data_json = json.dumps(top10_recomendados)

    # Criar a resposta JSONP, adicionando a função de callback ao início do objeto JSON
    response = callback + '(' + data_json + ')'

    # Retornar a resposta JSONP
    return response

if __name__ == '__main__':
    app.run()
