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

# COMMENT: This for building function
# website = 'https://twitter.com/search?q=python&src=typed_query'
# COMMENT: This for infinite scrolling
website = 'https://twitter.com/Support/status/1696328519817867558'

path = r'D:\RepoGithub\chromedriver-win64\chromedriver.exe'

options = Options()
options.add_argument("--no-sandbox")

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
driver.maximize_window()


# NOTE: LOAD USERNAME AND PASSWORD FROM .env
#  USE YOUR TWITTER ACCOUNT TO LOGIN
load_dotenv()

# NOTE: loginForm_button IS OPTIONAL. IT'S USED IN ACCESS LOGIN FORM IN INFINITE SCROLLING URL
loginForm_button = driver.find_element(By.XPATH, '//a[@href="/login"]')
loginForm_button.click()

username = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete = "username"]')))
username.send_keys(os.environ['TWITTER_USER'])

next_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]')
next_button.click()


password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete = "current-password"]')))
password.send_keys(os.environ['TWITTER_PASS'])

login_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Log in"]')
login_button.click()

time.sleep(2)



def get_tweet(element):
	# [x]: HANDLE EXCEPTION ELEMENT NOT FOUND
	try:
		user = element.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
		text = element.find_element(By.XPATH, ".//div[@lang]").text
		tweet_data = [user, text]
	except:
		tweet_data = ['', '']
	return tweet_data


user_data = []
text_data = []
tweet_ids = set()

scrolling = True
while scrolling:
	tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
	for tweet in tweets[-15:]:
		tweet_data = get_tweet(tweet)
		tweet_id = ''.join(tweet_data)
		if tweet_id not in tweet_ids:
			tweet_ids.add(tweet_id)
			user_data.append(tweet_data[0])
			text_data.append(" ".join(tweet_data[1].split()))

	# Get the initial scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
			scrolling = False
			break
		else:
			last_height = new_height
			break


df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets_infinite_scrolling.csv', index=False)
print(df_tweets)

input("Press Enter to close the browser...")
driver.quit()

