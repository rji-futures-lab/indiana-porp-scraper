import requests
from bs4 import BeautifulSoup
from models import RestrainingOrder
import os, re

files = [
	f for f in os.listdir(".cache/SearchDetail")
	if '.html' in f
	]
for file in files:
	print(file)

	ro_id = int(file[:-5])
	
	ro = RestrainingOrder.get(RestrainingOrder.id == ro_id)

	with open(f".cache/SearchDetail/{file}") as file:

		html = file.read()

	soup = BeautifulSoup(html, "html.parser")

	orders = soup.find('ul', {'class': 'orders'})
	details = soup.find('div', {'id': 'form-con'})

	try:
		place = details.find("p", text = re.compile('City:*')).text.replace('City:', '').strip()
	except AttributeError:
		pass
	else:
		ro.city = place.split(',')[0].strip()
		ro.state = place.split(',')[1].strip()

	lis = orders.find_all('li')
	library = {}


	for li in lis:
		p_tags = li.find_all('p')
		label = p_tags[0].find('strong').text.strip()
		if label == 'Attempted to serve respondent on:':
			ro.officer_notes = p_tags[0].find('span').text.replace('Officer Notes:', '').strip()
			
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
	except KeyError:
		pass 

	ro.save()


