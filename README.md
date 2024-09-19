# Web Scraping de Notebooks Lenovo com API RESTful

Este projeto consiste na criação de um **web scraper** que coleta informações de notebooks da marca **Lenovo** disponíveis no site [Webscraper Test E-commerce](https://webscraper.io/test-sites/e-commerce/static/computers/laptops). Além disso, os dados coletados são disponibilizados por meio de uma **API RESTful** em formato **JSON** para facilitar o consumo por outros serviços.

## Funcionalidades

- Coleta informações de todos os notebooks da marca **Lenovo**.
- Ordena os produtos do mais barato para o mais caro.
- Exibe todas as informações disponíveis dos notebooks, incluindo:
  - Título do produto.
  - Preço.
  - Quantidade de avaliações.
  - Link para o produto.
  - Descrição adicional e opções de armazenamento (se disponíveis).
- API RESTful para acessar os dados de maneira otimizada.
- Tratamento de exceções e erros de rede.

## Tecnologias Utilizadas

- **Python 3**
- **Django** com **Django REST Framework**
- **BeautifulSoup4** para o web scraping
- **Requests** para realizar as requisições HTTP
- **Git** para controle de versão
- **GitHub** como plataforma de hospedagem de código
