from db import RestrainingOrder
from bs4 import BeautifulSoup
import requests
import requests_cache
import string

initial_url ="https://mycourts.in.gov/porp"

r = requests.get(initial_url)








search_url = "https://mycourts.in.gov/PORP/Search/Results?PageSize=100000&PageIndex=0"

