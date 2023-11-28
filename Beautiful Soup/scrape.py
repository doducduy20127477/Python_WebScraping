from bs4 import BeautifulSoup
import requests
import re

root = 'https://subslikescript.com'
website = f'{root}/movies'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

# print(soup.prettify())

box = soup.find('article', class_='main-article')

links = []
for link in box.find_all('a', href=True):
	links.append(link['href'])

for link in links:
	website = f'{root}/{link}'
	result = requests.get(website)
	content = result.text
	soup = BeautifulSoup(content, 'lxml')

	box = soup.find('article', class_='main-article')
	title = box.find('h1').get_text()
	transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')
	# Remove characters not allowed in Windows file names
	title_cleaned = re.sub(r'[<>:"/\\|?*]', '', title)

	# print(title)
	# print(transcript)

	with open(f'{title_cleaned}.txt', 'w', encoding='utf-8') as file:
		file.write(transcript)

