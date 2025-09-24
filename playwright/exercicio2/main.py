import os
import json
from playwright.sync_api import sync_playwright

def scrape_quotes():
    # URL do site alvo
    url = "http://quotes.toscrape.com"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 1. Navegar para a pagina
            print(f"Acessando {url}...")
            page.goto(url)
            page.wait_for_load_state("networkidle")

            # 2. Encontrar todos os contêineres das citações
            # Cada citação está dentro de uma div com a classe 'quote'
            print("Extraindo citações da página...")
            quote_selectors = page.locator("div.quote")
            
            # Conta quantos elementos foram encontrados
            count = quote_selectors.count()
            print(f"Encontradas {count} citações.")

            # 3. Lista para armazenar os dados extraídos
            quotes_data = []

            # 4. Iterar sobre cada citação encontrada e extrair os dados
            for i in range(count):
                quote_element = quote_selectors.nth(i)
                
                text = quote_element.locator("span.text").inner_text()
                
                author = quote_element.locator("small.author").inner_text()
                
                #adiciona na lista
                quotes_data.append({
                    "frase": text,
                    "autor": author
                })
                
                print(f"- Frase de {author} extraída.")

            # 5. Salvar os dados em um arquivo JSON 
            # Descobre o diretório onde o script está localizado
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Cria o caminho completo para o arquivo
            output_filename = os.path.join(script_dir, "citacoes.json")
            
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(quotes_data, f, indent=4, ensure_ascii=False)
            
            print(f"\nDados salvos com sucesso no arquivo '{output_filename}'!")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            # Fechar o navegador
            print("Fechando o navegador.")
            browser.close()

if __name__ == "__main__":
    scrape_quotes()