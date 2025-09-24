import json
import time
import os
import sys
import io
import random
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Forçar saída UTF-8 no console para evitar erro com emojis ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- LÓGICA PARA ENCONTRAR O .ENV NA PASTA RAIZ ---
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
# --- fim da logica .ENV ---

# --- digitaçao mais humana ---
def type_like_human(element, text):
    """Digita um texto em um elemento, caractere por caractere, com atrasos aleatórios."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.08, 0.25))

# --- FUNÇÃO DE LOGIN ---
def login_instagram(usuario, senha):
    """
    Realiza o login no Instagram, lida com 2FA (com ajuda manual) e pop-ups.
    """
    print("Iniciando o navegador para login...")
    options = Options()
    options.add_argument("--start-maximized")
    # oculta log desnesseraios no 2fatores
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.instagram.com/")
        wait = WebDriverWait(driver, 15)

        campo_usuario = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        campo_senha = driver.find_element(By.NAME, "password")
        
        campo_usuario.clear()
        time.sleep(random.uniform(0.5, 1.0))
        type_like_human(campo_usuario, usuario)
        
        campo_senha.clear()
        time.sleep(random.uniform(0.5, 1.0))
        type_like_human(campo_senha, senha)
        
        botao_login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        time.sleep(random.uniform(0.8, 1.5))
        botao_login.click()
        # se tiver 2 etapas pede pra digitar no console se nao passa
        try:
            campo_2fa = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "verificationCode"))
            )
            print("\nATENÇÃO: Verificação de duas etapas detectada.")
            codigo_2fa = input("Por favor, digite o código de 6 dígitos que você recebeu e pressione Enter: ")
            type_like_human(campo_2fa, codigo_2fa.strip())
            botao_confirmar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirmar')]")))
            time.sleep(random.uniform(0.8, 1.5))
            botao_confirmar.click()
        except TimeoutException:
            print("Página de verificação de duas etapas (2FA) não detectada, continuando...")
            pass

        time.sleep(random.uniform(6.5, 8.2))
        # salvar infos se tiver
        try:
            salvar_info = driver.find_element(By.XPATH, "//div[contains(text(),'Agora não') or contains(text(),'Not Now')]")
            salvar_info.click()
            time.sleep(random.uniform(2.5, 3.8))
        except NoSuchElementException:
            pass
        # notificacoes se tiver
        try:
            notificacoes = driver.find_element(By.XPATH, "//button[contains(text(),'Agora não') or contains(text(),'Not Now')]")
            notificacoes.click()
            time.sleep(random.uniform(2.5, 3.8))
        except NoSuchElementException:
            pass
        # tudo certo manda mensagem
        print("Login realizado com sucesso.")
        return driver

    except (Exception, TimeoutException) as e:
        print(f"Ocorreu um erro inesperado durante o login: {e}")
        driver.quit()
        return None

# --- extrir os dados ---
def extrair_dados_perfil(driver, perfil="@computacaounifavip_"):
    """
    Navega até o perfil e extrai a Bio. Salva tudo em um arquivo JSON.
    """
    dados_perfil = {
        "perfil": perfil,
        "data_extracao": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        url_perfil = f"https://www.instagram.com/{perfil.strip('@')}/"
        print(f"\nNavegando para o perfil: {url_perfil}")
        driver.get(url_perfil)
        wait = WebDriverWait(driver, 15)
        # tenta pegar os dados da bio
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade")))
            bio_elements = driver.find_elements(By.CSS_SELECTOR, "span._ap3a._aaco._aacu._aacx._aad7._aade")
            bio_text = "\n".join([el.get_attribute("innerText").strip() for el in bio_elements if el.text.strip()])
            dados_perfil["bio"] = bio_text if bio_text else "Não encontrada ou perfil sem bio."
            print(f"  - Bio encontrada:\n{dados_perfil['bio']}")
        except (NoSuchElementException, TimeoutException):
            dados_perfil["bio"] = "Não encontrada ou perfil sem bio."
            print("  - Bio não encontrada.")
            
        # salva tudo no json na pasta correta 
        output_path = Path(__file__).parent / "dados_perfil_instagram.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dados_perfil, f, ensure_ascii=False, indent=4)

        print("\n--- DADOS EXTRAÍDOS COM SUCESSO ---")
        print(json.dumps(dados_perfil, indent=4, ensure_ascii=False))
        print("-------------------------------------")
        print(f"Dados salvos no arquivo '{output_path}'.")

    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a extração: {e}")
    finally:
        print("Fechando o navegador.")
        driver.quit()

# --- FUNÇÃO PRINCIPAL DO BOT ---
def run_login_and_extraction():
    """
    Função principal que chama as outras 2
    """
    # pega os dados do env para segurança
    usuario = os.getenv("INSTAGRAM_USER")
    senha = os.getenv("INSTAGRAM_PASS")

    #caso não tenha credenciais lança erro 
    if not usuario or not senha:
        print("ERRO: As credenciais INSTAGRAM_USER e INSTAGRAM_PASS não foram encontradas.")
        print("Verifique se o arquivo .env está na raiz do projeto e se as variáveis estão definidas.")
        return

    print("Iniciando processo de automação do Instagram (com login)...")
    driver_logado = login_instagram(usuario, senha)

    if driver_logado:
        extrair_dados_perfil(driver_logado)
    else:
        print("Não foi possível continuar com a extração de dados, pois o login falhou.")

# --- BLOCO PARA TESTE INDEPENDENTE ---
if __name__ == "__main__":
    print("--- Executando o bot do Instagram de forma independente para teste ---")
    run_login_and_extraction()
    print("--- Fim do teste ---")