import os
from bs4 import BeautifulSoup
from models import RestrainingOrder
from urllib.parse import urlparse

for f in os.listdir(".cache/SearchResults"):
	with open(f".cache/SearchResults/{f}") as file:
		html = file.read()
	soup = BeautifulSoup(html, "html.parser")
	

	tbody = soup.find('tbody')
	rows = tbody.find_all('tr')

	for row in rows:
		cells = row.find_all('td')
		url = cells[7].find('a')['href']
		parsed = urlparse(url)
		ro = RestrainingOrder.create(
			case_number=cells[6].text,
			name=cells[1].text,
			date_filed=cells[2].text,
			born=cells[3].text,
			race=cells[4].text,
			county=cells[5].text,
			id=int(parsed.query.strip('ID=')),
		)




