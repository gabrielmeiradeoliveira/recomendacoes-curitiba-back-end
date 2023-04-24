# Documentação do Código

[Documentação do crawler do tripadvisor](https://github.com/GabrielMeira01/recomendacoes-curitiba/blob/main/README-CRAWLER.md)

## Sobre o Código

O código apresentado é um servidor Flask que disponibiliza uma rota para recomendar restaurantes com base nas avaliações dos usuários. O servidor realiza a análise de sentimentos das avaliações dos restaurantes para encontrar os mais recomendados.

## Dependências

O código depende das seguintes bibliotecas:

- Flask
- json
- nltk

Para instalar as dependências, basta executar o seguinte comando no terminal:

pip install Flask nltk

## Como Executar o Código

Para executar o código, basta executar o seguinte comando no terminal:


Por padrão, o servidor será executado na porta 8000.

## Como Usar o Código

Para usar o código, basta fazer uma requisição GET para a rota "/recomendar" com os seguintes parâmetros:

- callback: nome da função de callback para JSONP
- feedback: texto contendo as palavras-chave para encontrar os restaurantes recomendados

O servidor irá retornar uma resposta JSONP contendo os top 5 restaurantes recomendados e a média de sentimentos das avaliações. Se houver menos de 5 restaurantes com sentimento positivo, o servidor irá retornar todos os restaurantes com sentimento positivo.

## Considerações Finais

A documentação apresentada é um guia básico para entender e utilizar o código. É importante lembrar que o código pode ser modificado e adaptado de acordo com as necessidades do projeto. Em caso de dúvidas ou sugestões, entre em contato com o autor do código. 
