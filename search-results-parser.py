import os
from bs4 import BeautifulSoup
from models import RestrainingOrder

for f in os.listdir(".cache"):
	with open(f".cache/{f}") as file:
		html = file.read()
	soup = BeautifulSoup(html, "html.parser")
	

	tbody = soup.find('tbody')
	rows = tbody.find_all('tr')

	for row in rows:
		cells = row.find_all('td')
		ro = RestrainingOrder()
		ro.case_number = cells[6].text
		ro.name = cells[1].text
		ro.date_filed = cells[2].text
		ro.born = cells[3].text
		ro.race = cells[4].text
		ro.county = cells[5].text
		ro.url = cells[7].text
		ro.save()
