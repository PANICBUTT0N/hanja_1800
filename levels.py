from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import time


def get_level(char):
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    
    driver.get('https://hanja.dict.naver.com/#/main')
    
    WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'keyword'))
    )

    input_element = driver.find_element(By.CLASS_NAME, 'keyword')
    input_element.clear()
    time.sleep(1)
    input_element.send_keys(char)
    input_element.send_keys(Keys.ENTER)

    pattern = r'\d+급(?:I{1,2})?'

    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, "//*[contains(text(), '읽기')]"))
        )
        reading_button = driver.find_element(By.XPATH, "//*[contains(text(), '읽기')]")
        reading_match = re.search(pattern, reading_button.text)

        if reading_match:
           reading_level = reading_match.group()
        else:
            reading_level = 'Could not retrieve reading level.'
        reading_level = reading_level.replace('급', '')
    except:
        print('Encountered error when retrieving reading level.')
        reading_level = 'Could not retrieve reading level.'

    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.XPATH, "//*[contains(text(), '쓰기')]"))
        )
        writing_button = driver.find_element(By.XPATH, "//*[contains(text(), '쓰기')]")
        writing_match = re.search(pattern, writing_button.text)

        if writing_match:
            writing_level = writing_match.group()
        else:
            writing_level = ''
        writing_level = writing_level.replace('급', '')
    except:
        writing_level = 'Could not retrieve writing level.'
        print('Encountered error when retrieving writing level.')
    return reading_level, writing_level
