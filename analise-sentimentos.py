import json
from textblob import TextBlob

def get_best_local(data, sentiment):
    """
    Retorna o melhor local com base no sentimento médio dos comentários e na pontuação de sentimento da frase de entrada.
    """
    best_score = -float('inf')
    best_local = None
    for local in data:
        reviews = local['reviews']
        if not reviews:
            continue

        local_sentiment = sum(TextBlob(review['content']).sentiment.polarity for review in reviews) / len(reviews)
        score = local_sentiment + sentiment
        if score > best_score:
            best_score = score
            best_local = local

    return best_local

def print_local_info(local):
    """Imprime informações do local"""
    name = local['name']
    address = local['address']
    phone = local['phone']
    cuisine = local['cuisine']
    price = local['price']
    print('Restaurante:')
    print('  Nome:', name)
    print('  Endereço:', address)
    print('  Telefone:', phone)
    print('  Tipo de cozinha:', cuisine)
    print('  Preço:', price)

def print_reviews(reviews, sentiment):
    """Imprime comentários relevantes com base no sentimento"""
    if sentiment > 0:
        print('\nComentários positivos:')
        relevant_reviews = [review['content'] for review in reviews if TextBlob(review['content']).sentiment.polarity > 0]
    elif sentiment < 0:
        print('\nComentários negativos:')
        relevant_reviews = [review['content'] for review in reviews if TextBlob(review['content']).sentiment.polarity < 0]
    else:
        print('\nAlguns comentários:')
        relevant_reviews = [review['content'] for review in reviews[:5]]
    for review in relevant_reviews:
        print(review)

def main():
    """Função principal para executar o programa"""
    # ler o arquivo JSON
    with open('locais.json') as f:
        data = json.load(f)

    # permitir que o usuário insira uma frase
    sentence = input('Digite uma frase para analisar: ').strip()

    # realizar a análise de sentimento
    blob = TextBlob(sentence)
    sentiment = blob.sentiment.polarity

    # encontrar o melhor local com base no sentimento médio dos comentários e na pontuação de sentimento da frase de entrada
    best_local = get_best_local(data, sentiment)

    # imprimir informações do melhor local e comentários relevantes
    print_local_info(best_local)
    print_reviews(best_local['reviews'], sentiment)

if __name__ == '__main__':
    main()
