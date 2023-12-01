from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

website = 'https://www.lazada.vn/shop-ca-phe-3-trong-1/?nestle-viet-nam&from=wangpu&m=shop&q=All-Products'
path = r'D:\RepoGithub\chromedriver-win64\chromedriver.exe'

options = Options()
options.add_argument("--no-sandbox") # needed, because colab runs as root

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)
driver.maximize_window()


# time.sleep(6)

# sigin_google = driver.find_element(By.XPATH, '//div[(@id="container")]/div[@role="button"]')
# sigin_google = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="button"]//span[text()="Sign in with Google"]')))
# sigin_google.click()




input("Press Enter to close the browser...")
driver.quit()

# df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
# df_books.to_csv('books_pagination.csv', index=False)