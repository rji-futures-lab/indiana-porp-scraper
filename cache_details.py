import argparse
from datetime import datetime
import os
from time import sleep
import requests


def make_requests(ids):
	with requests.Session() as sesh:
		for i in ids:
			ids.remove(i)
			start = datetime.now()
			url = f'https://mycourts.in.gov/PORP/Search/Detail?ID={i}'
			r = sesh.get(url)
			try:
				r.raise_for_status()
			except requests.exceptions.HTTPError as e:
				print(f'  {e}')
				sleep(120)
			else:
				html = r.content
				with open(f".cache/SearchDetail/{i}.html", 'wb') as file:
					file.write(html)
				duration = datetime.now() - start
				print(f'  cached {i} ({duration})')
				sleep(4)


def main():
	from recent_protection_orders import query
	from models import RestrainingOrder
	
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-s', '--start-id', nargs='?', type=int, dest='start_id'
	)
	parser.add_argument(
		'-e', '--end-id', nargs='?', type=int, dest='end_id'
	)
	args = parser.parse_args()
	
	os.makedirs('.cache/SearchDetail/', exist_ok=True)

	if args.start_id:
		query = query.where(RestrainingOrder.id >= args.start_id)
	if args.end_id:
		query = query.where(RestrainingOrder.id <= args.end_id)

	ids = [ro.id for ro in query]

	make_requests(ids)


if __name__ == "__main__":
    main()
