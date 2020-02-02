### python3 code/wikipedia_api_json_data.py --help
usage: wikipedia_api_json_data.py [-h] [--titles TITLES [TITLES ...]] size

Get JSON data from wikipedia REST API (summaries) related to specified initial
titles up to defined size. Script also prepares chunked files for load to
Elasticsearch via _bulk API.

positional arguments:
  size                  Size of raw json data to get (in bytes).

optional arguments:
  -h, --help            show this help message and exit
  --titles TITLES [TITLES ...]
                        Initial titles to which get the related content (space
                        separated). Make sure you specify valid titles.

*Example: python3 wikipedia_api_json_data.py 20971520 --titles Amazon_\(company\) Google Facebook Microsoft*