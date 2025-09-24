import datetime
import os
import json
from playwright.sync_api import sync_playwright, expect

def automate_login_and_save_result():
    # URL e credenciais
    url = "https://the-internet.herokuapp.com/login"
    username = "tomsmith"
    password = "SuperSecretPassword!"
    
    # Define o caminho de saída para o arquvio
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, "resultado_login.json")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 1. Acessar a página de login
            print(f"Acessando {url}...")
            page.goto(url)

            # 2. Preencher o formulário
            print("Preenchendo o formulário de login...")
            page.locator("input#username").fill(username)
            page.locator("input#password").fill(password)

            # 3. Clicar no botão de login
            print("Clicando no botão de login...")
            page.locator("button[type='submit']").click()

            # 4. Validar a mensagem de sucesso
            print("Validando a mensagem de sucesso...")
            success_message_locator = page.locator("div#flash")
            expect(success_message_locator).to_be_visible()
            expect(success_message_locator).to_contain_text("You logged into a secure area!")

            print("\nSUCESSO! A mensagem de login bem-sucedido foi validada.")
            
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            
            # 5. Extrair o texto e preparar os dados para o JSON
            message_text = success_message_locator.inner_text().strip()
            output_data = {
                "status": "Sucesso",
                "mensagem": message_text,
                "timestamp": current_timestamp
            }
            print(f"Texto extraído: '{message_text}'")

        except Exception as e:
            print(f"\nFALHA! Ocorreu um erro durante a execução: {e}")
            output_data = {
                "status": "Falha",
                "erro": str(e),
                "timestamp": current_timestamp
            }
        
        finally:
            # 6. Salvar o resultado (sucesso ou falha) no arquivo JSON
            if 'output_data' in locals():
                with open(output_filename, "w", encoding="utf-8") as f:
                    json.dump(output_data, f, indent=4, ensure_ascii=False)
                print(f"Resultado salvo no arquivo '{output_filename}'")

            # Pausa para ver o resultado antes de fechar
            page.wait_for_timeout(2000)
            # Fechar o navegador
            print("Fechando o navegador.")
            browser.close()


if __name__ == "__main__":
    automate_login_and_save_result()