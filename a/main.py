from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configura el driver (asegúrate de tener el driver adecuado, como ChromeDriver, en tu PATH)
navegador = webdriver.Chrome()

try:
    # Abre Google
    navegador.get("https://www.google.com")

    # Encuentra el cuadro de búsqueda
    search_box = navegador.find_element(By.NAME, "q")

    # Escribe una consulta y presiona Enter
    search_box.send_keys("Wero09Anano" + Keys.RETURN)

    # Espera unos segundos para ver los resultados
    time.sleep(40)

    # Extrae los títulos de los primeros resultados
    results = navegador.find_elements(By.XPATH, "//h3")
    for index, result in enumerate(results[:5], start=1):
        print(f"{index}. {result.text}")

finally:
    # Cierra el navegador
    navegador.quit()
