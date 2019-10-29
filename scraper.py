from models import RestrainingOrder
from bs4 import BeautifulSoup
import requests
import string

base_url = 'https://mycourts.in.gov/PORP/'
results_url = base_url + 'Search/Results'
form_data = {
    'SearchMode':'LastName'
}

with requests.Session() as sesh:
    init_get_r = sesh.get(base_url)
    init_get_r.raise_for_status()
    for letter in string.ascii_lowercase:
    	form_data["RespondentNameLast"] = letter
    	post_r = sesh.post(base_url, data=form_data)
    	post_r.raise_for_status()
    
    	get_results_r = sesh.get(results_url, params={'PageSize': 99999})
    	get_results_r.raise_for_status()

    	with open(f'.cache/results-for-{letter}.html', 'wb') as f:
    		f.write(get_results_r.content)
    	




