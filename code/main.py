import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Carregar o conteúdo do arquivo cidades.json
with open('cidades.json', 'r', encoding='utf-8') as file:
    cidades = json.load(file)

# Criar uma lista para armazenar os dados
dados = []

# Loop através dos estados e municípios
for estado, municipios in cidades.items():
    for municipio_dict in municipios:
        municipio = municipio_dict["municipio"]
        
        # Concatenar a URL com o primeiro município do arquivo
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        url = f'https://sensacaotermica.com/{municipio}'
        
        # Fazer a requisição GET
        response = requests.get(url, headers=header)
        
        # Parsear o conteúdo HTML
        soup = BeautifulSoup(response.content, 'html.parser')
                
        # Encontra os elementos com as informações de temperatura e sensação térmica
        temperatura_element = soup.find('div', class_='col-4 col-6 col-lg-4 temperatura').find('div', class_='numero')
        sensacao_termica_element = soup.find('div', class_='col-4 col-6 col-lg-4 sensacao').find('div', class_='numero')
        
        # Extrai o texto das tags encontradas
        temperatura = temperatura_element.text.strip()
        sensacao_termica = sensacao_termica_element.text.strip()
        
        # Obter a data da extração
        data_extracao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Adicionar os dados à lista
        dados.append({
            'Estado': estado,
            'Município': municipio,
            'Temperatura': temperatura,
            'Sensação Térmica': sensacao_termica,
            'Data da Extração': data_extracao
        })

# Criar um DataFrame com os dados
df = pd.DataFrame(dados)

# Exibir as 50 primeiras linhas do DataFrame
print(df.head(10))

# Exportar o DataFrame para um arquivo CSV
df.to_csv('dados_climaticos.csv', index=False, encoding="ISO-8859-1")
