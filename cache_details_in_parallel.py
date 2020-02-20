import argparse
import multiprocessing
import os
from time import sleep
import requests
from recent_protection_orders import query


session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def get_session():
    return session


def cache_page(identifier):
    sleep(3)
    url = f'https://mycourts.in.gov/PORP/Search/Detail?ID={identifier}'
    r = get_session().get(url)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'  {e}')
        sleep(120)
        session = requests.Session()
    else:
        html = r.content
        file_path = f".cache/SearchDetail/{identifier}.html"
        with open(file_path, 'wb') as file:
            file.write(html)
        return print(f'  Cached content from {url} (in {id(get_session())})')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cache each protection order details page.",
    )
    parser.add_argument(
        '--num_processes', type=int, default=os.cpu_count()
    )

    pool_config = {
        'processes': parser.parse_args().num_processes,
        'initializer': set_global_session,
    }
    
    os.makedirs('.cache/SearchDetail/', exist_ok=True)

    with multiprocessing.Pool(**pool_config) as pool:
        pool.map(cache_page, query)
