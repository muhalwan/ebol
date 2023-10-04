import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

companies_df = pd.read_csv("Input/data_perusahaan.csv")
results = []

driver = webdriver.Chrome()

base_url = "https://kemenperin.go.id/direktori-perusahaan?what={}&prov=0"


def save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("Output/Company_KBLI_Results.csv", index=False)


for company in companies_df['Nama']:
    url = base_url.format(company)
    driver.get(url)

    try:
        code_element = driver.find_element(By.XPATH, '//tr[@bgcolor="white"]/td[3]')
        code = code_element.text
        results.append({'Company': company, 'KBLI': code})
    except NoSuchElementException:
        results.append({'Company': company, 'KBLI': 'Not Found'})
    except Exception as e:
        save_to_csv(results)
        driver.close()
        raise e

driver.close()
save_to_csv(results)
