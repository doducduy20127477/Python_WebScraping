from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

options = Options()
options.add_argument("--headless")
options.headless = True
options.add_argument('window-size=1920x1080')
options.add_argument("--no-sandbox")

website = 'https://www.audible.com/search'
path = r'D:\RepoGithub\chromedriver-win64\chromedriver.exe'

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
# driver.maximize_window()

container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

book_title = []
book_author = []
book_length = []

for product in products:
	title = product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text
	book_title.append(title)
	print(title)
	book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
	book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

driver.quit()

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_headless.csv', index=False)
