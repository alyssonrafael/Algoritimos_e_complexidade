import os
from playwright.sync_api import sync_playwright, TimeoutError

def youtube_search_and_screenshot_v3():
    with sync_playwright() as p:
        # Abrir o navegador
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 1. Navegar para o YouTube
            print("Navegando para o YouTube...")
            page.goto("https://www.youtube.com")

            # 2. Lidar com o Pop-up de Consentimento de Cookies
            try:
                print("Procurando o pop-up de consentimento...")
                accept_button = page.get_by_role("button", name="Accept all").or_(page.get_by_role("button", name="Aceitar tudo"))
                accept_button.wait_for(timeout=5000)
                accept_button.click()
                print("Pop-up de consentimento aceito.")
            except TimeoutError:
                print("Nenhum pop-up de consentimento encontrado ou já foi aceito. Continuando...")

            # 3. 4 segundos antes de pesquisar
            print("Aguardando 4 segundos antes de pesquisar...")
            page.wait_for_timeout(4000)

            # 4. Pesquisar por mrbeast
            print("Pesquisando por MrBeast...")
            search_input_selector = 'input[name="search_query"]'
            page.wait_for_selector(search_input_selector, state='visible', timeout=10000)
            page.fill(search_input_selector, "MrBeast")
            page.press(search_input_selector, "Enter")
            
            # 5. Esperar a página de resultados carregar
            page.wait_for_load_state("networkidle")

            # 6. espera para tirar o print
            page.wait_for_timeout(3000)

            # 7. tirar o print
            # Descobre o diretório onde o script está sendo executado
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Cria o caminho completo para salvar o print no canto certo
            screenshot_path = os.path.join(script_dir, "mrbeast_print.png")
            
            print(f"Tirando screenshot e salvando em {screenshot_path}...")
            page.screenshot(path=screenshot_path)
            print("Screenshot tirado com sucesso!")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            # Fechar o navegador
            print("Fechando o navegador.")
            browser.close()

if __name__ == "__main__":
    youtube_search_and_screenshot_v3()