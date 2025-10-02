# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys

# URL do curso que será analisado
URL_CURSO = 'https://www.cursoemvideo.com/curso/python-3-mundo-1/'

print("Iniciando raspagem de dados...")

try:
    # Cabeçalho para simular um navegador
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
    # Baixa e analisa a página principal do curso
    response = requests.get(URL_CURSO, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Lista para armazenar os dados coletados
    dados_finais = []

    # Seleciona todos os elementos que representam um "bloco" de módulo
    modulos = soup.select('.ld-item-list-item.ld-item-lesson-item')

    if not modulos:
        print("Nenhum módulo foi encontrado. A estrutura do site pode ter mudado.")
        sys.exit()

    # Itera sobre cada bloco de módulo para extrair seus dados
    for modulo in modulos:
        titulo_modulo_tag = modulo.select_one('.ld-item-title')
        titulo_modulo = titulo_modulo_tag.find(text=True, recursive=False).strip()
        
        # Encontra todas as aulas dentro do módulo
        aulas = modulo.select('.ld-table-list-item a')
        
        for aula in aulas:
            # Coleta o título da aula e o link da página da aula
            titulo_aula = aula.select_one('.ld-topic-title').get_text(strip=True)
            link_pagina_aula = aula['href']
            
            # Adiciona os dados à lista final
            dados_finais.append({
                "Módulo": titulo_modulo,
                "Aula": titulo_aula,
                "Link": link_pagina_aula,
            })

    # Define o nome do arquivo de saída
    nome_arquivo = f"lista_aulas_{URL_CURSO.strip('/').split('/')[-1]}.txt"
    
    # Salva os resultados no arquivo de texto
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        modulo_atual = ""
        for item in dados_finais:
            # Escreve o nome do módulo sempre que ele mudar
            if item["Módulo"] != modulo_atual:
                modulo_atual = item["Módulo"]
                f.write("\n" + "="*60 + "\n")
                f.write(f"MÓDULO: {modulo_atual}\n")
                f.write("="*60 + "\n")
            
            # Escreve os dados da aula
            f.write(f"  - Aula: {item['Aula']}\n")
            f.write(f"    Link: {item['Link']}\n\n")

    print("Processo finalizado com sucesso!")

except requests.exceptions.RequestException as e:
    print(f"\nOcorreu um erro de conexão: {e}")
except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")