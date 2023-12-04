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


website = 'https://twitter.com/search?q=python&src=typed_query'
path = r'D:\RepoGithub\chromedriver-win64\chromedriver.exe'

options = Options()
options.add_argument("--no-sandbox")

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
driver.maximize_window()


# LOAD USERNAME AND PASSWORD FROM .env
# USE YOUR TWITTER ACCOUNT TO LOGIN
load_dotenv()

username = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete = "username"]')))
username.send_keys(os.environ['TWITTER_USER'])

next_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]')
next_button.click()


password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete = "current-password"]')))
password.send_keys(os.environ['TWITTER_PASS'])

login_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Log in"]')
login_button.click()

def get_tweet(element):
	# COMMENT: HANDLE EXCEPTION ELEMENT NOT FOUND
	try:
		user = element.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
		text = element.find_element(By.XPATH, ".//div[@lang]").text
		tweet_data = [user, text]
	except:
		tweet_data = ['', '']
	return tweet_data

tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))

user_data = []
text_data = []
for tweet in tweets:
	tweet_data = get_tweet(tweet)
	user_data.append(tweet_data[0])
	text_data.append(" ".join(tweet_data[1].split()))


df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets.csv', index=False)
print(df_tweets)

input("Press Enter to close the browser...")
driver.quit()

