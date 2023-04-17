Abra o Postman e crie uma nova solicitação GET.

Na barra de endereço, insira a URL onde a API está sendo executada, por exemplo, http://localhost:5000/recomendar.

Na seção de parâmetros, adicione dois parâmetros: callback e feedback.


O valor do parâmetro callback deve ser o nome da função JavaScript que você deseja chamar com o resultado da API. O valor do parâmetro feedback deve ser uma frase contendo feedback sobre um restaurante, por exemplo, "gostei do restaurante".


Clique no botão "Enviar" para enviar a solicitação.
Exemplo de solicitação GET:

GET http://localhost:5000/recomendar?callback=minha_funcao&feedback=gostei%20do%20restaurante

Observe que o parâmetro feedback deve ser codificado como uma string válida para URL. No exemplo acima, o espaço foi codificado como %20.

Se a API estiver sendo executada corretamente e sem erros, a resposta será um objeto JSONP contendo os 10 restaurantes mais recomendados, com base no feedback fornecido e nas avaliações disponíveis no arquivo _locais.json. O resultado será passado para a função JavaScript especificada no parâmetro callback.

Exemplo de resposta JSONP:

minha_funcao([["Restaurante A", 0.8], ["Restaurante B", 0.6], ["Restaurante C", 0.5], ... ])
