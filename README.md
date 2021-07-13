## Contextualização do negócio 

House Rocket é uma plataforma digital que tem como modelo de negócio a compra e venda de imóveis usando tecnologia. Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e portanto maior sua receita. Entretanto, as casas possuem muitos atributos que as tornam mais ou menos atrativas aos compradores e vendedores e a localização e o período do ano também podem influenciar os preços.

Esse projeto esta publicado no Heroku https://house-rocket.herokuapp.com/

**OBS:Esse é um projetoi fictício.**

## Questão de negócio

Diante desse contexto, busca-se responder as seguintes questões: 

    1 - Quais são os imóveis que deveria comprar e por qual preço ?

    2 - Uma vez o imóvel comprado, qual o melhor momento para vendê-lo e por qual preço ?

## Atributos 

Os dados para desenvolver esse projeto de insights foram retirados do Kaggle¹. Em suma, esse dataset é formado por linhas e colunas, onde cada coluna é um atributo e seu significado está explicado na tabela abaixo.

¹ https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885

## Premissas do negócio 

Algumas premissas foram levantadas com uma rápida visualização geral dos dados:

  - a coluna yr_renovated com valores igual a zero, significa que as casas nunca foram reformadas

  - as casas com waterfront igual a zero, quer dizer que não possuem vista para água.

  - as colunas de floors e bathrooms possuem números fracionários, isso não tem sentido físico, deveriávamos perguntar o que isso significa em termos imobiliários.

  - ID com 33 bathrooms é um erro na tabela

## Planejamento da Solução

O planejamento da solução segui-se da maneira abaixo, vale salientar que as ferramentas utilizadas foram o Python 3.8, Jupyter Notebook, Jupyter Lab, Sublime Text, Streamlit e Heroku. Todas as bibliotecas necessárias para esse projeto estão no requiments.txt

  - Coleta dos dados: Kaggle

  - Entendimento dos negócio
		
  - Tratamento dos dados: Etapa realizada para transformar, limpar e entender os dados para levar hipóteses para o time de negócio.

  - Levantamento de hipóteses

  - Exploração de dados: Etapa que busca verificar se as hipóteses geradas são falsas ou verdadeiras. Além disso, busca-se as correlações entre as váriasveis e a váriavel resposta. Aqui também podemos gerar hipóteses mais profundas sobre os dados.

  - Levantamento dos principais Insights encontrados

  - Tradução para o negócio: Depois da verificação das hipóteses, buscou-se analisar seu significado para o negócio em si.

  - Conclusão: Respostas para as perguntas de negócio.

## Hipóteses 

    H1 = O preço dos imóveis crescem 10% MoM na média
    H2 = Imóveis nunca reformados são 15% mais baratos na média 
    H3 = A estação summer apresenta preços 30% mais caros na média que as outras estações do ano
    H4 = Os imóveis com vista para água na estação summer são 40% na média mais caros que os com vista para aguá no winter 
    H5 = Imóveis com vista para água são em média 30% mais caros

## Insights 

Apenas as hipóteses H2 e H5 foram verdadeiras. Com a visualização dos dados podemos observar e retirar alguns insights relevantes para o negócio, os quais estão apresentados abaixo.

    - Imóveis com vista para água não possuem um grande dependencia da estação do ano em preço.
    - Imóveis com vista para água são mais caros na média. 
    - Imóveis sem reforma são mais baratos na média.

## Tradução para o negócio 

Nessa etapa traduzimos o que as hipóteses dizem para a linguagem de negócio:

    H1 = O preço dos imóveis crescem 10% MoM na média: FALSA. Os preços dos imóveis sofrem uma flutuação natural com o decorrer dos meses. Deve-se analisar mais profundamente quais fatos locais impactaram nesses preços históricos.
    
    H2 = Imóveis nunca reformados são 15% mais baratos na média: VERDADEIRA. Deve-se investir em imóveis nunca reformados com vista para água, assim conseguimos colocar uma maior porcentagem de lucro em cima do preço de venda.
    
    H3 = A estação summer apresenta preços 30% mais caros na média que as outras estações do ano: FALSA. Podemos investir em imóveis em qualquer época do ano, já que o que influencia no preço são as caracteristicas locais e fisicas do imóvel.
    
    H4 = Os imóveis com vista para água na estação summer são 40% na média mais caros que os com vista para aguá no winter: FALSA. Podemos comprar e vendar imóveis com vista para água em qualquer momendo do ano.
    
    H5 = Imóveis com vista para água são em média 30% mais caros: VERDADEIRA. Ou seja, as caracteristicas da localização afetam nos preços dos imóveis. Dessa forma, imóveis com vsita para água traram um maior lucro se usarmos essa localiação a nosso favor como estratégia de venda.


## Próximo passos
Responder a questão abaixo:

    3 - A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças?


