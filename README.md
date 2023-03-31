# Análise de Sentimentos do TripAdvisor

Este projeto em Python tem como objetivo coletar dados do site TripAdvisor e fazer uma análise de sentimentos para recomendar um lugar. O código utiliza a biblioteca BeautifulSoup para analisar o HTML das páginas do TripAdvisor e a biblioteca Selenium para automatizar o processo de navegação pelas páginas.

# Pré-requisitos

Para executar este projeto, é necessário ter as seguintes bibliotecas instaladas:

BeautifulSoup
Selenium
Pandas
JSON
Também é necessário ter o driver do Firefox instalado em seu sistema. Você pode baixá-lo em https://github.com/mozilla/geckodriver/releases.

# Como usar

Clone este repositório em seu computador
Instale as bibliotecas necessárias
Baixe o driver do Firefox e adicione o diretório do driver ao PATH do sistema
Execute o arquivo tripadvisor.py
Aguarde o processo de coleta e análise de dados ser concluído
Verifique o arquivo locais.json gerado com as informações coletadas e analisadas
# Como funciona

O código acessa a página de resultados da busca no TripAdvisor e coleta os links para as cinco primeiras páginas de restaurantes. Em seguida, o código visita cada página de restaurante, coleta as informações do local e as avaliações de usuários.

As avaliações são submetidas a uma análise de sentimentos utilizando a biblioteca NLTK. A análise retorna uma pontuação de sentimento para cada avaliação, que é adicionada a uma lista de pontuações para o local. A pontuação final do local é calculada como a média das pontuações de todas as avaliações.

Ao final, o código recomenda o local com a pontuação de sentimento mais alta.
