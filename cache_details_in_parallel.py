import argparse
import multiprocessing
import os
from time import sleep
from recent_protection_orders import query
from cache_details import make_requests


def get_chunks(num_chunks):
    total = query.count()
    chunk_size = round(total / num_chunks)
    # For item i in a range that is the count of the query,
    for i in range(0, total, chunk_size):
        # Create an index range for l of n items:
        yield query[i:i+chunk_size]


def handle_chunk(ids):
    make_requests(ids)
    sleep(30)
    

def download_all_chunks(chunks):
    num_pools = len(chunks)
    with multiprocessing.Pool(num_pools) as pool:
        pool.map(handle_chunk, chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('num_processes', type=int)
    args = parser.parse_args()
    
    os.makedirs('.cache/SearchDetail/', exist_ok=True)
    
    chunks = list(
        get_chunks(args.num_processes)
    )

    download_all_chunks(chunks)
