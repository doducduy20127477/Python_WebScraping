from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.add_argument("--headless")
options.headless = False
# options.add_argument('window-size=1920x1080')
# options.add_argument("--no-sandbox")

website = 'https://www.audible.com/adblbestsellers?ref_pageloadid=djOWEIt7wJ8JfJnK&ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=d42ea6af-6ce9-44e1-bbd5-7e2e15acab17&pf_rd_r=CKTJNB9FTWFYZCZBF6RB&pageLoadId=kY3lt6IHzMZKx4Kv&ref_plink=not_applicable&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482'
path = r'D:\RepoGithub\chromedriver-win64\chromedriver.exe'

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.maximize_window()

#pagination
# wait = WebDriverWait(driver, 10)
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')
# pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "pagingElements")]')))

pages = pagination.find_elements(By.TAG_NAME, 'li')
# print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + pagination.text)
last_page = int(pages[-2].text)
# last_page_text = pages[-2].text
# last_page = int(last_page_text) if last_page_text.strip() else 1

current_page = 1


book_title = []
book_author = []
book_length = []

while current_page <= last_page:
	# time.sleep(2)
	# container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
	# products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')
	container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
	products = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class, "productListItem")]')))

	for product in products:
		title = product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text
		book_title.append(title)
		# print(title)
		book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
		book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

	current_page = current_page + 1

	try:
		next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
		next_page.click()
	except:
		pass

driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_pagination.csv', index=False)
