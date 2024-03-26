import requests
from bs4 import BeautifulSoup

def buscar_fipe(placa):
    # Construa a URL corretamente usando a placa fornecida
    url = f"https://placafipe.com/placa/{placa}/"
    
    try:
        # Faça uma solicitação GET para a URL para obter o conteúdo HTML
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        
        # Verifique se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Crie um objeto BeautifulSoup com o conteúdo HTML da página
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Encontre os elementos HTML relevantes para os dados da Fipe
            results = soup.findAll("td", {"width": "50px"})
            return results
        elif response.status_code == 403:
            print(f'Erro 403: Acesso negado para a placa {placa}')    
        else:
            # Se houver um erro na solicitação, imprima uma mensagem de erro
            print(f'Erro na solicitação GET usando a placa: {placa}:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        # Se ocorrer uma exceção durante a solicitação, imprima a mensagem de erro
        print(f'Erro durante a solicitação GET usando a placa: {placa}:', e)
        return None

# Exemplo de uso da função

