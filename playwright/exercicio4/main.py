import os
import csv
from playwright.sync_api import sync_playwright

def scrape_mercado_livre_challenge_v2():
    # produto
    search_term = "notebook"
    
    # caminho de saída para o arquivo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, "produtos_mercadolivre.csv")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 1. Acessar o Mercado Livre
            print("Acessando o Mercado Livre...")
            page.goto("https://www.mercadolivre.com.br/")

            # Opcional: Lidar com o pop-up de cookies se ele aparecer
            try:
                page.get_by_role("button", name="Aceitar cookies").click(timeout=3000)
                print("Pop-up de cookies aceito.")
            except Exception:
                print("Nenhum pop-up de cookies encontrado.")

            # 2. Pesquisar pelo produto
            print(f"Pesquisando por '{search_term}'...")
            search_bar_selector = "input.nav-search-input"
            page.locator(search_bar_selector).fill(search_term)
            page.keyboard.press("Enter")

            # 3. Esperar a página de resultados carregar
            print("Aguardando a página de resultados...")
            results_container_selector = "ol.ui-search-layout"
            page.wait_for_selector(results_container_selector, timeout=20000)

            # 4. Localizar todos os itens de resultado
            product_items = page.locator("li.ui-search-layout__item")
            count = product_items.count()
            print(f"Encontrados {count} resultados. Capturando os 5 primeiros...")

            # 5. Lista para armazenar os dados
            products_data = []

            # 6. Extrair nome e preço dos 5 primeiros
            for i in range(min(5, count)):
                product = product_items.nth(i)
                
                name = "Nome não encontrado"
                price = "Preço não encontrado"

                try:
                    # Seletor para o título do produto
                    name_selector = ".poly-component__title"
                    name = product.locator(name_selector).first.inner_text()
                except Exception:
                    print(f"Não foi possível extrair o nome para o produto {i+1}")

                try:
                    # Seletor para o preço (parte inteira e centavos)
                    price_fraction_selector = ".andes-money-amount__fraction"
                    price_fraction = product.locator(price_fraction_selector).first.inner_text()
                    
                    cents_selector = ".andes-money-amount__cents"
                    if product.locator(cents_selector).count() > 0:
                        price_cents = product.locator(cents_selector).first.inner_text()
                        price = f"R$ {price_fraction},{price_cents}"
                    else:
                        price = f"R$ {price_fraction}"
                except Exception:
                    print(f"Não foi possível extrair o preço para: {name}")

                products_data.append({
                    "Nome do Produto": name,
                    "Preço": price
                })
                print(f"  - Produto {i+1}: {name} | {price}")

            # 7. Salvar os dados em um arquivo CSV
            print(f"\nSalvando os dados em '{output_filename}'...")
            headers = ["Nome do Produto", "Preço"]
            with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(products_data)
            
            print("Dados salvos com sucesso!")

        except Exception as e:
            print(f"Ocorreu um erro geral: {e}")
        finally:
            page.wait_for_timeout(3000)
            print("Fechando o navegador.")
            browser.close()

if __name__ == "__main__":
    scrape_mercado_livre_challenge_v2()