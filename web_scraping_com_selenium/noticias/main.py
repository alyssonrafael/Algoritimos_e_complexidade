import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_news_scraper(url="https://g1.globo.com/", limite=10):
    """
    Coleta as principais manchetes do G1 usando Selenium, exibe no console
    e salva em um arquivo JSON.
    """
    print(f"\nIniciando o navegador para coletar notícias em: {url}")
    
    options = Options()
    options.add_argument("--start-maximized")
    # A linha abaixo executa o navegador em segundo plano (sem interface gráfica)
    # Descomente para uma execução mais rápida e discreta.
    # options.add_argument("--headless") 
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        # Espera explicitamente até 15 segundos para que os posts do feed sejam carregados
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "feed-post-body")))

        # Encontra todos os posts visíveis na página, limitado pelo `limite`
        posts = driver.find_elements(By.CLASS_NAME, "feed-post-body")[:limite]

        manchetes_coletadas = []
        for post in posts:
            try:
                # Tenta encontrar o link e o título dentro de cada post
                link_tag = post.find_element(By.CLASS_NAME, "feed-post-link")
                titulo = link_tag.text.strip()
                link = link_tag.get_attribute("href")
                
                # O resumo é opcional, então usamos um try/except para ele
                try:
                    resumo_tag = post.find_element(By.CLASS_NAME, "feed-post-body-resumo")
                    resumo = resumo_tag.text.strip()
                except NoSuchElementException:
                    resumo = "" # Define como vazio se não encontrar

                if titulo and link:
                    manchetes_coletadas.append({
                        "titulo": titulo,
                        "link": link,
                        "resumo": resumo,
                        "data_coleta": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
            except NoSuchElementException:
                # Se um post não tiver a estrutura esperada, pula para o próximo
                print("AVISO: Um post foi encontrado com estrutura diferente e será ignorado.")
                continue

        if manchetes_coletadas:
            print("\n--- Principais Manchetes do G1 (Coletadas com Selenium) ---")
            for i, item in enumerate(manchetes_coletadas, 1):
                print(f"{i}. {item['titulo']}")
            print("----------------------------------------------------------")

            output_path = Path(__file__).parent / "manchetes_g1_selenium.json"
            with open(output_path, mode="w", encoding="utf-8") as arquivo_json:
                json.dump(manchetes_coletadas, arquivo_json, ensure_ascii=False, indent=4)

            print(f"Arquivo '{output_path.name}' salvo com sucesso na pasta 'noticias'.")
        else:
            print("Nenhuma manchete encontrada. O layout do site pode ter sido alterado.")

    except TimeoutException:
        print("Erro: A página demorou muito para carregar ou os posts não foram encontrados a tempo.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        print("Fechando o navegador.")
        driver.quit()

# Bloco para permitir a execução independente deste script para testes
if __name__ == "__main__":
    print("--- Executando o scraper de notícias com Selenium (modo de teste) ---")
    run_news_scraper()
    print("--- Fim da execução de teste ---")