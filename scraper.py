import os
import string
import requests


base_url = 'https://mycourts.in.gov/PORP/'
results_url = base_url + 'Search/Results'
form_data = {
    'SearchMode':'LastName'
}


with requests.Session() as sesh:
    init_get_r = sesh.get(base_url)
    init_get_r.raise_for_status()

    letters_in_cache = [
        f[12] for f in os.listdir('.cache') if '.html' in f
    ]

    letters_to_request = [
        l for l in string.ascii_lowercase if l not in letters_in_cache
    ]

    for letter in letters_to_request:

        form_data['RespondentNameLast'] = letter

        post_r = sesh.post(base_url, data=form_data)
        try:
            post_r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'POST request failed for {letter}')
            print(e)
        else:
            get_results_r = sesh.get(results_url, params={'PageSize': 99999})
            try:
                get_results_r.raise_for_status()
            except requests.exceptions.HTTPError:
                print(f'GET request failed for {letter}')
                print(e)
            else:
                with open(f'.cache/results-for-{letter}.html', 'wb') as f:
                    f.write(get_results_r.content)
