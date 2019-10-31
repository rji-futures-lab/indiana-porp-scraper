
	soup = BeautifulSoup(html, "html.parser")

	orders = soup.find('ul', {'class': 'orders'})


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

	print(library)




	ro.date_issued = library['Order issued on:']
	try:
		ro.date_served = library['Respondent successfully served on:']
	except KeyError:
		pass
	try:
		ro.order_dismissed_on = library['Order dismissed on']
	except KeyError:
		pass
	try:
		ro.order_expired_on = library['Order expired on:']
	except KeyError:
		pass
	try:
		ro.dismissal_reason = library['Dismissal Reason']
	except KeyError:
		pass
	ro.save()

	sleep(2)
