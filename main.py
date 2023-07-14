from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://ecolana.com.mx/mapa")

nombre = []
residuos = []
direccion = []
telefono = []
horario = []
mapsUrl = []
try:
    elements = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="map"]/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div/img')))
    
    # elements = browser.find_elements(By.XPATH, '//*[@id="map"]/div/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div')
    
    for element in elements:
        # Ejecuta un click por javascript
        browser.execute_script("arguments[0].click();", element)
        # Esperar por puntos en el mapa
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/h2')))
        nombre.append(browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/h2').text)
        residuos.append(browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div/div[1]/div[1]/p').text)
        direccion.append(browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div/div[1]/div[2]/div[2]/p').text)
        
        checkHor = browser.find_elements(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div/h4')
        if(len(checkHor) != 0):
            horario.append(browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div/h4').text)
        else:
            horario.append("")
        
        checkTel = browser.find_elements(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div/div[1]/div[2]/div[4]/p')
        if(len(checkTel) != 0):
            telefono.append(browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div/div[1]/div[2]/div[4]/p').text)
        else:
            telefono.append("")
            
        browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[2]/div[2]/img').click()
        browser.switch_to.window(browser.window_handles[1])
        
        try:
            
            mapsUrl.append(browser.current_url)
            
        except Exception as e:
            
            print("fallo.")
            if(len(nombre) != len(mapsUrl)):
                mapsUrl.append(browser.current_url)
            
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/button').click()
finally:
    browser.quit()
    
archivo_csv = 'C:/Users/Fabia/OneDrive/Desktop/ecolanaData.csv'


with open(archivo_csv, mode='w', encoding='utf-8', newline='') as file:
   
    writer = csv.writer(file)

    # Titulos en csv
    writer.writerow(['Nombre', 'Residuos', 'Dirección', 'Teléfono', 'Horario de servicio', 'URL'])

    # Datos
    for i in range(len(nombre)):
        writer.writerow([nombre[i], residuos[i], direccion[i], telefono[i], horario[i], mapsUrl[i]])


