import requests
from bs4 import BeautifulSoup



url = 'https://mycourts.in.gov/PORP/Search/Detail?ID=876939'

### need to replace url line with 
### something that can re-iterate through enire DB. something like
## base_url

r = requests.get(url)

html = r.text

soup = BeautifulSoup(html, "html.parser")

date_issued = soup.find('p', {'class': 'date'})

date_served = soup.find_all('p',{'class': 'date'})
##above line needs method making it the second "date" tag, not the first
print(date_served)

print(date_issued)

order_dismissed_on = soup.find('p', {'class': 'date dismissed'})

print(order_dismissed_on)