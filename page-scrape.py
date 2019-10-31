import requests
from bs4 import BeautifulSoup
from models import RestrainingOrder
from time import sleep

query = RestrainingOrder.select().where(
	(
		RestrainingOrder.date_filed.endswith('2017') | 
		RestrainingOrder.date_filed.endswith('2018') | 
		RestrainingOrder.date_filed.endswith('2019')
	) & RestrainingOrder.case_number.contains('PO')
)
	# url = f'https://mycourts.in.gov/PORP/Search/Detail?ID={ro.id}'
	# r = requests.get(url)
	# html = r.content
	# with open(f".cache/SearchDetails/{f}.html", 'w') as file:
	# 	html = file.write()
	# sleep(2)

print(query.count())