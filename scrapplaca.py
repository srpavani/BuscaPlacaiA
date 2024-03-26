import requests
import re
from bs4 import BeautifulSoup

def buscar_fipe(placa):
    url = f"https://placafipe.com/placa/{placa}/"
    
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            resultados = soup.findAll("td", {"width": "50px"})
            valores = []
            for resultado in resultados:
                valor = re.search(r'R\$\s*([\d,.]+)', resultado.text)
                if valor:
                    valores.append(valor.group(1).replace(',', '.'))
            return valores
            
        elif response.status_code == 403:
            print(f'Erro 403: Acesso negado para a placa {placa}')    
        else:
            print(f'Erro na solicitação GET usando a placa: {placa}:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print(f'Erro durante a solicitação GET usando a placa: {placa}:', e)
    
