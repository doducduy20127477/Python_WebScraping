from selenium import webdriver
from selenium.webdriver.chrome.service import Service

website = 'https://www.adamchoi.co.uk/overs/detailed'
path = '/home/hcm-mki-l2077/Downloads'

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.headless = True

# service = Service(executable_path=r'/home/hcm-mki-l2077/Downloads')

driver = webdriver.Chrome(path)
driver.get(website)


driver.quit()