from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

options = Options()
# options.add_argument("--headless")
# options.headless = True
# options.add_argument('window-size=1920x1080')
options.add_argument("--no-sandbox")

website = 'https://www.lazada.vn/shop-ca-phe-3-trong-1/?nestle-viet-nam&from=wangpu&m=shop&q=All-Products'
path = r'D:\RepoGithub\chromedriver-win64\chromedriver.exe'

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
driver.maximize_window()

#pagination
# wait = WebDriverWait(driver, 10)
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "ant-pagination")]')
# pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "pagingElements")]')))

pages = pagination.find_elements(By.TAG_NAME, 'li')
# print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + pagination.text)
last_page = int(pages[-2].text)
# print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' + pages[-2].text)

# last_page_text = pages[-2].text
# last_page = int(last_page_text) if last_page_text.strip() else 1

current_page = 1


product_name = []
product_price = []
product_sold = []
product_reviews = []
product_gifts = []


while current_page <= last_page:
	container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@data-qa-locator= "general-products"]')))
	products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/div[@data-qa-locator= "product-item"]')))


	for product in products:
		try:
			name_element = product.find_element(By.XPATH, './/a[@title]')
			name = name_element.text
		except NoSuchElementException:
			name = ""

		try:
			price_element = product.find_element(By.XPATH, './/span[contains(text(), "₫")]')
			price = price_element.text
		except NoSuchElementException:
			price = 0

		try:
			sold_element = product.find_element(By.XPATH, './/span[contains(text(), "Đã bán")]')
			sold = sold_element.text
		except NoSuchElementException:
			sold = 0

		try:
			reviews_element = product.find_element(By.XPATH, './/span[contains(text(), "(")]')
			reviews = reviews_element.text
		except NoSuchElementException:
			reviews = 0

		product_name.append(name)
		product_price.append(price)
		product_sold.append(sold)
		product_reviews.append(reviews)

	current_page = current_page + 1

	try:
		next_page = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//li[contains(@class, "ant-pagination-next")]')))

		# next_page = driver.find_element(By.XPATH, '//li[contains(@class, "ant-pagination-next")]')
		# driver.execute_script("window.scrollBy(0, 200)")
		# next_page.click()
		driver.execute_script("arguments[0].click();", next_page)
	except Exception as e:
		print(f"An error occurred: {e}")
		pass




driver.quit()

df_books = pd.DataFrame({'name': product_name, 'price': product_price, 'sold': product_sold, 'reviews': product_reviews})
df_books.to_csv('products.csv', index=False)
