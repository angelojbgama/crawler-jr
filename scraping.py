import requests
from bs4 import BeautifulSoup

# URL do site
URL = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'

def get_lenovo_notebooks():
    # Fazendo a requisição HTTP para obter o conteúdo da página
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Lista para armazenar os dados dos notebooks
    notebooks = []
    
    # Encontra todos os produtos na página
    products = soup.find_all('div', class_='thumbnail')
    
    for product in products:
        # Extrair título, preço, descrição e número de avaliações
        title = product.find('a', class_='title').text.strip()
        price = product.find('h4', class_='price').text.strip()
        description = product.find('p', class_='description').text.strip()
        reviews = product.find('p', class_='pull-right').text.strip()
        
        # Verifica se o notebook é da marca Lenovo
        if 'Lenovo' in title:
            # Adiciona o produto à lista de notebooks
            notebooks.append({
                'title': title,
                'price': float(price.replace('$', '')),
                'description': description,
                'reviews': reviews
            })
    
    # Ordenar os notebooks pelo preço (do mais barato para o mais caro)
    notebooks_sorted = sorted(notebooks, key=lambda x: x['price'])
    
    return notebooks_sorted

# Testar a função
if __name__ == '__main__':
    lenovo_notebooks = get_lenovo_notebooks()
    
    # Exibir os notebooks Lenovo ordenados
    for notebook in lenovo_notebooks:
        print(f"Nome: {notebook['title']}")
        print(f"Preço: ${notebook['price']}")
        print(f"Descrição: {notebook['description']}")
        print(f"Avaliações: {notebook['reviews']}")
        print('---')
