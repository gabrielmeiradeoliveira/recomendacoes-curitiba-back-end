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

# Definir um filtro de idioma para as stopwords em português
stopwords_pt = set(stopwords.words('portuguese'))

# Definir novos scores de pontuação
sia.lexicon.update({
    'ótimo': 2.5,
    'excelente': 2.5,
    'perfeito': 2.5,
    'maravilhoso': 2.5,
    'incrível': 2.5,

    'ruim': -2.5,
    'horrível': -2.5,
    'péssimo': -2.5,
    'terrível': -2.5,
    'desagradável': -2.5,
    'inadequado': -2.5,
    'inferior': -2.5,
    'reprovado': -2.5,
    'mau': -2.5,
    'falho': -2.5,
    'falha': -2.5,
    'mediocre': -2.0,
    'insuficientemente': -2.0,
    'inferioridade': -2.0,
    'não é bom': -1.5,
    'não é ótimo': -2.5,
    'não é excelente': -2.5,
    'não é recomendado': -1.5,
    'não é suficiente': -1.5,
    'não é suficientemente': -1.5,
    'não é aceitável': -1.5,
    'não é aprovado': -2.5,
    'não é razoável': -1.5,
    'não é legal': -1.5,
    'não é incrível': -2.5,
    'não é adequado': -1.5,
    'não é excepcional': -2.5,
    'não é surpreendente': -1.5,
    'não é fantástico': -2.5,
    'não é bom o suficiente': -1.5,
    'não é satisfatório': -1.5,
    'não é agradável': -2.5,
    'não é brilhante': -2.5,
    'não é magnífico': -2.5,
    'não é extraordinário': -2.5,
    'não é recomendável': -1.5,
    'muito bom': 2.5,
    'muito legal': 2.0,
    'muito recomendado': 2.0,
    'muito aprovado': 2.0,
    'muito adequado': 2.0,
    'muito razoável': 2.0,
    'muito aceitável': 2.0,
    'muito surpreendente': 2.5,
})

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
with open('restaurante_meu.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False, separators=(',', ':'))
