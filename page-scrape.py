import os
import requests
from bs4 import BeautifulSoup
from models import RestrainingOrder
from time import sleep


os.makedirs('.cache/SearchDetail/', exist_ok=True)


query = RestrainingOrder.select().where(
	(
		RestrainingOrder.date_filed.endswith('2017') | 
		RestrainingOrder.date_filed.endswith('2018') | 
		RestrainingOrder.date_filed.endswith('2019')
	) & RestrainingOrder.case_number.contains('PO')
)

for ro in query:

	url = f'https://mycourts.in.gov/PORP/Search/Detail?ID={ro.id}'
	print(url)
	r = requests.get(url)
	html = r.content
	with open(f".cache/SearchDetail/{ro.id}.html", 'wb') as file:
		file.write(html)
	sleep(2)
