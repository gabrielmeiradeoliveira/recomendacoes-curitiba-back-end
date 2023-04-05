import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# carregar o arquivo JSON
with open('locais.json', encoding='utf-8' ) as f:
    data = json.load(f)

# inicializar o analisador de sentimentos
sia = SentimentIntensityAnalyzer()

# iterar sobre cada restaurante
for restaurante in data:
    # iterar sobre cada avaliação
    for avaliacao in restaurante['reviews']:
        # obter o texto da avaliação
        texto = avaliacao['content']
        # tokenizar o texto
        tokens = nltk.word_tokenize(texto)
        # calcular o sentimento da avaliação
        sentimento = sia.polarity_scores(texto)['compound']
        # adicionar o sentimento à avaliação
        avaliacao['sentimento'] = sentimento
    
    # adicionar o número de avaliações positivas, negativas e neutras
    n_pos = len([a for a in restaurante['reviews'] if a['sentimento'] > 0])
    n_neg = len([a for a in restaurante['reviews'] if a['sentimento'] < 0])
    n_neu = len([a for a in restaurante['reviews'] if a['sentimento'] == 0])
    restaurante['n_pos'] = n_pos
    restaurante['n_neg'] = n_neg
    restaurante['n_neu'] = n_neu
    
        # adicionar o sentimento geral do restaurante
    total_sentimento = sum([a['sentimento'] for a in restaurante['reviews']])
    if len(restaurante['reviews']) > 0:
        sentimento_medio = total_sentimento / len(restaurante['reviews'])
    else:
        sentimento_medio = 0 # ou "sem classificação"
    restaurante['sentimento_medio'] = sentimento_medio

    
# salvar o arquivo JSON modificado
with open('restaurante_meu.json', 'w', encoding='utf-8') as f:
    json.dump(data, f,  indent=2, ensure_ascii=False)
