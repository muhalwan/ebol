import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

kbli_df = pd.read_csv("KBLI_Coding.csv", encoding='latin1')
companies_df = pd.read_csv("Perusahaan_Coding.csv", encoding='latin1')

url = "https://kemenperin.go.id/direktori-perusahaan"

driver = webdriver.Chrome(executable_path='E:\\Code\\Scrap\\pt\\chromedriver.exe')

driver.get(url)

kbli_codes = []

for company in companies_df['Company']:
    search_box = driver.find_element(By.NAME, "what")
    search_box.clear()
    search_box.send_keys(company)
    driver.find_element(By.XPATH, '//input[@type="submit"]').click()
    time.sleep(2)

    try:
        code = driver.find_element(By.XPATH, '//td[text()="\d{5}"]').text
    except:
        code = None
    kbli_codes.append(code)
    driver.get(url)

companies_df['KBLI'] = kbli_codes

def get_classes(kbli):
    try:
        classes = kbli_df[kbli_df['KBLI'] == kbli][['Class 1', 'Class 2', 'Class 3', 'Class 4']].values[0]
        return classes
    except:
        return [None, None, None, None]


companies_df['Class 1'], companies_df['Class 2'], companies_df['Class 3'], companies_df['Class 4'] = zip(
    *companies_df['KBLI'].map(get_classes))

companies_df.to_csv('Output.csv', index=False)

driver.quit()
