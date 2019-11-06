import requests
from bs4 import BeautifulSoup
from models import RestrainingOrder
import os, re

files = [
	f for f in os.listdir(".cache/SearchDetail")
	if '.html' in f
	]
for file in files:

	for f in files:
		ro_id = int(f[:-5])

		ro = RestrainingOrder.get(RestrainingOrder.id == ro_id)
		print(ro_id)

		with open(f".cache/SearchDetail/{f}") as file:

			html = file.read()

		soup = BeautifulSoup(html, "html.parser")

		orders = soup.find('ul', {'class': 'orders'})
		details = soup.find('div', {'id': 'form-con'})


		# city = details.find_all("p", {"p" : re.compile('City.*')})
		# print(city)

		lis = orders.find_all('li')
		library = {}


		for li in lis:
			p_tags = li.find_all('p')
			label = p_tags[0].text.strip()
			try:
				data = p_tags[1].text.strip()
			except IndexError:
				ro.not_served=True
			library[label] = data

		ro.date_issued = library['Order issued on:']
		try:
			ro.date_served = library['Respondent successfully served on:'].strip()
		except KeyError:
			pass
		try:
			ro.order_dismissed_on = library['Order dismissed on'].strip()
		except KeyError:
			pass
		try:
			ro.order_expired_on = library['Order expired on:'].strip()
		except KeyError:
			pass
		try:
			ro.dismissal_reason = library['Dismissal Reason'].strip()
		except KeyError:
			pass
		try:
			ro.attempted_serve = library['Attempted to serve respondent on:'].strip()

		ro.save()
		print(ro.date_issued)


