from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()

website = 'https://twitter.com/i/flow/login'
path = r'D:\RepoGithub\chromedriver-win64\chromedriver.exe'

options = Options()
options.add_argument("--no-sandbox")

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
driver.maximize_window()

# LOAD USERNAME AND PASSWORD FROM .env
# USE YOUR TWITTER ACCOUNT TO LOGIN
username = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete = "username"]')))
username.send_keys(os.environ['TWITTER_USER'])

next_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]')
next_button.click()


password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete = "current-password"]')))
password.send_keys(os.environ['TWITTER_PASS'])

login_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Log in"]')
login_button.click()



input("Press Enter to close the browser...")
driver.quit()
