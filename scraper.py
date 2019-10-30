import os
import string
import requests


# make a directory called ".cache" with a sub-directory called "SearchResults"
# (if they don't exist already)
# https://docs.python.org/3.7/library/os.html#os.makedirs
os.makedirs('.cache/SearchResults/', exist_ok=True)

# declare URLs to which we'll be sending requests
base_url = 'https://mycourts.in.gov/PORP/'
results_url = base_url + 'Search/Results'
# pre-populate the form_data we need to send with POST request
# https://requests.kennethreitz.org/en/master/user/quickstart/#make-a-request
form_data = {
    'SearchMode':'LastName'
}

# make a list of the letters for which there are cached search results
letters_in_cache = [
    f for f in os.listdir('.cache/SearchResults/') if '.html' in f
]

# make another list of letters WITHOUT cached search results
letters_to_request = [
    l for l in string.ascii_lowercase if l not in letters_in_cache
]

# instantiate a Session object to persist cookies, etc. across all requests
# https://requests.kennethreitz.org/en/master/user/advanced/#session-objects
with requests.Session() as sesh:
    # make a GET request to the page with the search form
    # this gets us a cookie with an ASP.NET_SessionId, etc.
    init_get_r = sesh.get(base_url)
    # raise an exception (i.e., stop everything) if we have a bad response
    init_get_r.raise_for_status()

    # loop over letters we need
    for letter in letters_to_request:
        # fill in the last name field on the search form
        form_data['RespondentNameLast'] = letter
        # make a POST request 
        post_r = sesh.post(base_url, data=form_data)
        # if we get a bad response, print exception, and go to the next letter
        try:
            post_r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'POST request failed for {letter}')
            print(e)
        else:
            # if the response is good, make another GET request
            # this time, maximize the number of results shown on the page
            get_results_r = sesh.get(results_url, params={'PageSize': 99999})
            # if we get a bad response, print the exception, and go to the next letter
            try:
                get_results_r.raise_for_status()
            except requests.exceptions.HTTPError:
                print(f'GET request failed for {letter}')
                print(e)
            else:
                # if the response is good, cache the search results
                with open(f'.cache/SearchResults/{letter}.html', 'wb') as f:
                    f.write(get_results_r.content)
