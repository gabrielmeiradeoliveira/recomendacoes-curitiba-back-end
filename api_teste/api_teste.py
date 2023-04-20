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

    recomendados = []
    for restaurante in data:
        # Análise de sentimento das avaliações que contêm as palavras digitadas pelo usuário
        avaliacoes = restaurante["reviews"]
        
        sentimento_avaliacoes = []
        for review in avaliacoes:
            conteudo = review["content"].lower()
            if all(palavra in conteudo for palavra in feedback.split()):
                # Se todas as palavras da entrada do usuário estão contidas na avaliação, calcular o sentimento
                sentimento_avaliacoes.append(sia.polarity_scores(conteudo)["compound"])
        if sentimento_avaliacoes:
            # Se houver pelo menos uma avaliação com todas as palavras da entrada do usuário, calcular a média de sentimentos
            media_sentimento = sum(sentimento_avaliacoes) / len(sentimento_avaliacoes)
            # Adicionar o restaurante à lista de recomendados com base na média de sentimentos
            recomendados.append((restaurante, media_sentimento))
    
    # Classificando a lista de restaurantes recomendados com base na média de sentimentos
    if recomendados:
        recomendados = sorted(recomendados, key=lambda r: r[1], reverse=True)
    
    # Retornando os restaurantes com sentimento mais positivo
    top_recomendados = []
    for restaurante, media_sentimento in recomendados:
        if media_sentimento > 0:
            top_recomendados.append((restaurante, media_sentimento))
        else:
            break
    
    # Retornando os top 10 restaurantes recomendados
    top5_recomendados = top_recomendados[:5]

    # Criar um objeto JSON com os restaurantes recomendados
    data_json = json.dumps(top5_recomendados)

    # Criar a resposta JSONP, adicionando a função de callback ao início do objeto JSON
    response = callback + '(' + data_json + ')'

    # Retornar a resposta JSONP
    return response

if __name__ == '__main__':
    app.run()
