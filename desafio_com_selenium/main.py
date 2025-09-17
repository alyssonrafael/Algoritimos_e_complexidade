from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging

# Configuração do log
logging.basicConfig(filename='desafio_com_selenium/login_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Configurações para rodar em segundo plano
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Inicializa o driver com as opções
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://the-internet.herokuapp.com/login")
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    message_element = driver.find_element(By.ID, "flash")
    message_text = message_element.text.strip()

    logging.info(f"Mensagem capturada: {message_text}")
    print("Login realizado. Mensagem registrada no log.")

except Exception as e:
    logging.error(f"Erro durante o processo: {str(e)}")
    print("Ocorreu um erro. Verifique o log.")

finally:
    driver.quit()
