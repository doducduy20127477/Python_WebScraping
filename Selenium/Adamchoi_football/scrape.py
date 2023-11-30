from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

website = 'https://www.adamchoi.co.uk/overs/detailed'
path = r'D:\RepoGithub\chromedriver-win64\chromedriver.exe'

try:
	# service = Service(executable_path=r'/home/hcm-mki-l2077/Downloads')
	service = Service(executable_path=path) # selenium 4
	# options = Options()
	# options.add_argument("--headless") # or use pyvirtualdiplay
	# options.add_argument("--no-sandbox") # needed, because colab runs as root

	# options.headless = True
	driver = webdriver.Chrome(service=service) # selenium 4

	# driver = webdriver.Chrome(path)
	driver.get(website)

	all_matches_button = driver.find_element(by="xpath", value='//label[@analytics-event="All matches"]')
	all_matches_button.click()

	dropdown = Select(driver.find_element(by="id", value='country'))
	dropdown.select_by_visible_text('Spain')
	time.sleep(3)

	matches = driver.find_elements(by="tag name", value='tr')
	date = []
	home_team = []
	score = []
	away_team = []
	for match in matches:
		# print(match.text)
		# print(match.find_element(by="xpath", value='./td[1]').text)
		date.append(match.find_element(by="xpath", value='./td[1]').text)
		home = match.find_element(by="xpath", value='./td[2]').text
		home_team.append(home)
		# print(home)
		score.append(match.find_element(by="xpath", value='./td[3]').text)
		away_team.append(match.find_element(by="xpath", value='./td[4]').text)

	df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
	df.to_csv('football_data.csv', index=False)
	print(df)

except Exception as e:
    print(f"An exception occurred: {str(e)}")
finally:
	# pass
	# input("Press Enter to close the browser...")
	driver.quit()


