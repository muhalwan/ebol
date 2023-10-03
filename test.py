import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


companies_df = pd.read_csv("Perusahaan_Coding.csv")
results = []

driver = webdriver.Chrome()

base_url = "https://kemenperin.go.id/direktori-perusahaan?what={}&prov=0"

for company in companies_df['Nama']:
    url = base_url.format(company)
    driver.get(url)

    try:
        code_element = driver.find_element(By.XPATH, '//tr[@bgcolor="white"]/td[3]')
        code = code_element.text
        results.append({'Company': company, 'KBLI': code})
    except NoSuchElementException:
        results.append({'Company': company, 'KBLI': 'Not Found'})


driver.close()


results_df = pd.DataFrame(results)
results_df.to_csv("Company_KBLI_Results.csv", index=False)