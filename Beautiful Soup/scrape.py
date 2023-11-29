from bs4 import BeautifulSoup
import requests
import re

root = 'https://subslikescript.com'
website = f'{root}/movies_letter-A'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())

#pagination
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

links = []
for page in range(1, int(last_page)+1)[:2]:
	root = 'https://subslikescript.com'
	result = requests.get(f'{website}?page={page}')
	content = result.text
	soup = BeautifulSoup(content, 'lxml')

	box = soup.find('article', class_='main-article')


	for link in box.find_all('a', href=True):
		links.append(link['href'])

	for link in links:
		try:
			print(link)
			result = requests.get(f'{root}/{link}')
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
		except:
			print('------------------ Link not working ------------------')
			print(link)



