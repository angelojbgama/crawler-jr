from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup

URL_BASE = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
PAGINAS = 20
VALORES_INCREMENTO = [0, 20, 40, 60, 80]

class NotebooksAPIView(APIView):

    def buscar_pagina(self, url):
        try:
            resposta = requests.get(url)
            resposta.raise_for_status()
            return resposta.text
        except requests.RequestException as e:
            raise Exception(f"Erro ao buscar a página: {e}")

    def analisar_produto(self, div_produto):
        try:
            titulo = div_produto.select_one('.title').get_text(strip=True)
            preco = float(div_produto.select_one('.price').get_text(strip=True).replace('$', '').replace(',', ''))
            contagem_avaliacoes = int(div_produto.select_one('.review-count').get_text(strip=True).split()[0])
            link = div_produto.select_one('.title')['href']
            return {
                'title': titulo,
                'price': preco,
                'review_count': contagem_avaliacoes,
                'link': link,
            }
        except (AttributeError, ValueError) as e:
            print(f"Erro ao analisar o produto: {e}")
            return None

    def coletar_detalhes_produto(self, link_produto, preco_original):
        url_produto = f"https://webscraper.io{link_produto}"
        conteudo_pagina = self.buscar_pagina(url_produto)
        sopa = BeautifulSoup(conteudo_pagina, 'html.parser')

        titulo_adicional = self.obter_texto_ou_nulo(sopa, '.title.card-title')
        descricao_adicional = self.obter_texto_ou_nulo(sopa, '.description')

        opcoes_armazenamento = self.obter_opcoes_armazenamento(sopa, preco_original)

        return {
            'additional_title': titulo_adicional,
            'additional_description': descricao_adicional,
            'storage_options': opcoes_armazenamento,
        }

    def obter_texto_ou_nulo(self, sopa, seletor):
        elemento = sopa.select_one(seletor)
        return elemento.get_text(strip=True) if elemento else None

    def obter_opcoes_armazenamento(self, sopa, preco_original):
        opcoes_armazenamento = {}
        for idx, botao in enumerate(sopa.select('.swatches button.swatch')):
            valor = botao['value']
            if valor and idx < len(VALORES_INCREMENTO):
                preco_armazenamento = preco_original + VALORES_INCREMENTO[idx]
                opcoes_armazenamento[valor] = preco_armazenamento
        return opcoes_armazenamento

    def coletar_notebooks(self):
        todos_produtos = []
        for pagina in range(1, PAGINAS + 1):
            url = f"{URL_BASE}?page={pagina}"
            conteudo_pagina = self.buscar_pagina(url)
            sopa = BeautifulSoup(conteudo_pagina, 'html.parser')
            divs_produto = sopa.select('.col-md-4.col-xl-4.col-lg-4')

            for div_produto in divs_produto:
                info_produto = self.analisar_produto(div_produto)
                if info_produto and "Lenovo" in info_produto['title']:
                    detalhes = self.coletar_detalhes_produto(info_produto['link'], info_produto['price'])
                    
                    # Atualizar o título com 'additional_title', se disponível
                    if detalhes['additional_title']:
                        info_produto['title'] = detalhes['additional_title']
                    
                    info_produto.update({
                        'description': detalhes['additional_description'],
                        'storage_options': detalhes['storage_options'],
                    })
                    
                    todos_produtos.append(info_produto)
        return todos_produtos

    def get(self, request):
        try:
            notebooks = self.coletar_notebooks()
            notebooks_ordenados = sorted(notebooks, key=lambda x: x['price'])
            return Response(notebooks_ordenados, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
