from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup

class NotebooksAPIView(APIView):

    def get(self, request):
        base_url_laptops = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={}'
        base_url_product = 'https://webscraper.io/test-sites/e-commerce/static/product/{}'
        total_laptop_pages = 20
        total_product_pages = 147
        notebooks = {}

        try:
            # Parte 1: Coletar todos os notebooks das páginas de laptops
            for page_num in range(1, total_laptop_pages + 1):
                url = base_url_laptops.format(page_num)
                response = requests.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'lxml')
                products = soup.find_all('div', class_='card thumbnail')

                for product in products:
                    title = product.find('a', class_='title').text.strip()
                    
                    # Filtra apenas notebooks Lenovo
                    if 'Lenovo' in title:
                        price = float(product.find('h4', class_='price').text.strip().replace('$', ''))
                        description = product.find('p', class_='description').text.strip()
                        reviews = product.find('p', class_='review-count').text.strip()
                        rating = len(product.find_all('span', class_='ws-icon-star'))
                        img_src = product.find('img', class_='image')['src']
                        
                        if title not in notebooks:
                            notebooks[title] = {
                                'title': title,
                                'price': price,
                                'description': description,
                                'reviews': reviews,
                                'rating': rating,
                                'image_url': f"https://webscraper.io{img_src}",
                                'memory_options': []
                            }

            # Parte 2: Acessar produtos individuais para pegar detalhes adicionais
            for product_id in range(1, total_product_pages + 1):
                url = base_url_product.format(product_id)
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'lxml')
                title = soup.find('h4', class_='title').text.strip()
                
                # Filtra apenas notebooks Lenovo
                if 'Lenovo' in title:
                    price = float(soup.find('h4', class_='price').text.strip().replace('$', ''))
                    description = soup.find('p', class_='description').text.strip()
                    reviews = soup.find('p', class_='review-count').text.strip()
                    rating = len(soup.find_all('span', class_='ws-icon-star'))
                    img_src = soup.find('img', class_='image')['src']
                    
                    memory_buttons = soup.find_all('button', class_='btn swatch')
                    memory_options = [button.get('value') for button in memory_buttons if not button.get('disabled')]
                    
                    if title in notebooks:
                        notebooks[title]['price'] = min(notebooks[title]['price'], price)
                        notebooks[title]['description'] = description
                        notebooks[title]['reviews'] = reviews
                        notebooks[title]['rating'] = max(notebooks[title]['rating'], rating)
                        notebooks[title]['memory_options'] = list(set(notebooks[title]['memory_options'] + memory_options))
                    else:
                        notebooks[title] = {
                            'title': title,
                            'price': price,
                            'description': description,
                            'reviews': reviews,
                            'rating': rating,
                            'image_url': f"https://webscraper.io{img_src}",
                            'memory_options': memory_options
                        }

            # Converta o dicionário para uma lista
            merged_notebooks = list(notebooks.values())

            return Response(merged_notebooks, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({'error': f'Erro ao acessar o site: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({'error': f'Erro ao processar os dados: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
