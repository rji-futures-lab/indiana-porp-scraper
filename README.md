# Indiana PORP Scraper

Code for collecting protection order registry data for the state of Indiana.

## ETL Process

The source of the data is the [PORP section](https://mycourts.in.gov/PORP/) of the Indiana Court Information Technology Extranet (aka, INcite).

To collect all available records, we submit the search form once for every possible last name initial. We then cache each results set.

```sh
python cache_search_results.py
```

Note that the above script requires an internet connection.

Next, we iterate over all the cached results, parsing restraining order records out of the html and storing them in a sqlite database.

```sh
python extract_search_results.py
```

Since we're working with cached web pages, this extraction step doesn't require an internet connection.

The search results don't include all available data for each restraining order, so we make an additional request for the details page of each restraining order. Once again, we cache these web pages.

```sh
python cache_details.py
```

By default, cache_details.py will loop over all the restraining orders (excluding those already in the cache) and make a `GET` request for each order's details page.

When running the scraper as a single process, this script will take an inordinate amount of time. The main problem is the server behind mycourts.in.gov, which can take up to a minute to respond even to these simple `GET` requests. To collect the entire data set, which is over half a million records, the script would have to run non-stop for six to seven months.

We can speed all this up by running parallel processes for caching these details pages. In so doing, we also need to make sure we aren't duplicating our requests.

Thus, cache_details.py accepts a `start-id` and/or `end-id`, allowing you to set up multiple, non-overlapping processes in separate terminal windows/tabs:

```sh
python cache_details.py -s=1296495 -e=1604007
```

For greater convenience, invoke another script: cache_details_in_parallel.py, specifying the number of parallel processes you want. Trial and error suggests that mycourts.in.gov will tolerate around 10 parallel processes without throwing too many `500` responses.

```sh
python cache_details_in_parallel.py 10
```

It's enough to make you wonder how many concurrent human users this website—ostensibly intended to support the law enforcement and court systems of an entire state—can actually support.

**Important Note:** When cache_details.py or cache_details_in_parallel.py catches a 500 response, it will skip that restraining order and continue to run. As such, it's a good idea to re-run the details page caching script in order to see if you get good responses the second time around. If not, then these remaining restraining orders probably warrant further investigation by a human operator.
