import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

# Baixar os dados de tokenização em português
nltk.download('punkt')

# Carregar o arquivo JSON
with open('_locais.json', encoding='utf-8') as f:
    data = json.load(f)

# Inicializar o analisador de sentimentos
sia = SentimentIntensityAnalyzer()

# Ler o arquivo com as novas pontuações
with open('_scores.json', 'r') as f:
    new_scores = json.load(f)

# Atualizar o objeto sia.lexicon com as novas pontuações
sia.lexicon.update(new_scores)

# Definir um filtro de idioma para as stopwords em português
stopwords_pt = set(stopwords.words('portuguese'))

# Iterar sobre cada restaurante
for restaurante in data:
    # Iterar sobre cada avaliação
    for avaliacao in restaurante['reviews']:
        # Obter o texto da avaliação
        texto = avaliacao['content']
        # Tokenizar o texto em português
        tokens = nltk.word_tokenize(texto, language='portuguese')
        # Remover as stopwords em português
        tokens = [t.lower() for t in tokens if t.lower() not in stopwords_pt]
        # Juntar os tokens limpos em um texto novamente
        texto_limpo = ' '.join(tokens)
        # Calcular o sentimento do texto limpo
        sentimento = sia.polarity_scores(texto_limpo)['compound']
        # Adicionar o sentimento à avaliação
        avaliacao['sentimento'] = sentimento
    
    # Adicionar o número de avaliações positivas, negativas e neutras
    n_pos, n_neg, n_neu = 0, 0, 0
    for avaliacao in restaurante['reviews']:
        sentimento = avaliacao.get('sentimento', 0)
        if sentimento > 0:
            n_pos += 1
        elif sentimento < 0:
            n_neg += 1
        else:
            n_neu += 1
    restaurante.update({'n_pos': n_pos, 'n_neg': n_neg, 'n_neu': n_neu})
    
    # Adicionar o sentimento geral do restaurante
    total_sentimento = sum([a['sentimento'] for a in restaurante['reviews']])
    sentimento_medio = total_sentimento / len(restaurante['reviews']) if len(restaurante['reviews']) > 0 else 0
    restaurante['sentimento_medio'] = sentimento_medio

# Salvar o arquivo JSON modificado
with open('_analise.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
