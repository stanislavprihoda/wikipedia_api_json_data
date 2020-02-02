import os, sys
import json
import datetime, time
import urllib.parse
import itertools
from concurrent.futures import ThreadPoolExecutor
import logging
import argparse

try:
    import requests
except ModuleNotFoundError:
    print("-----------------------------------------------------")
    print("Missing modules. Run: pip install -r requirements.txt")
    print("-----------------------------------------------------")

LOG_LEVEL = logging.INFO
MAX_WORKERS = 10
MAX_BATCH_SIZE = 50
BULK_FILE_SIZE = 10485760

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=LOG_LEVEL)
_logger = logging.getLogger(__name__)

api_random = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
api_related = "https://en.wikipedia.org/api/rest_v1/page/related/{}"
api_summary = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
#API_URL_metadata = "https://en.wikipedia.org/api/rest_v1/page/metadata/{}"

data_path = "data"
if not os.path.exists(data_path): os.makedirs(data_path)
bulk_filename = (os.path.join(data_path,f"wiki_{i}.bulk") for i in itertools.count(1))
data_filename = os.path.join(data_path,"wiki.data")

def generate(size=1024,initial_titles=None):
    _logger.info(f"Starting with size {size} and initial title {initial_titles}")
    start = time.time()
    data = list()
    if not initial_titles: data.append(get_random())
    else: data.extend(get_summary(initial_titles))
    processed_titles = set()
    backlog = list()
    fdata = open(data_filename, "w")
    fbulk = open(next(bulk_filename), "w")
    try:
        while True:
            for doc in data:
                _title = doc["titles"]["canonical"]
                _pageid = doc["pageid"]
                if fdata.tell()>size: raise SizeReached
                if _title in processed_titles: continue
                doc["@timestamp"] = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone().replace(microsecond=0).isoformat() #iso timestamp
                json.dump(doc,fdata)
                fdata.write('\n')
                json.dump({ "index" : { "_id" : str(_pageid) } }, fbulk)
                fbulk.write('\n')
                json.dump(doc, fbulk)
                fbulk.write('\n')
                processed_titles.add(_title)
                backlog.append(_title)
            batch, backlog = backlog[:MAX_BATCH_SIZE], backlog[MAX_BATCH_SIZE:]
            data_list = _run_parallel(MAX_WORKERS, get_related, batch)
            data = list(itertools.chain.from_iterable(data_list))
            if fbulk.tell()>=BULK_FILE_SIZE: fbulk = _increment_file_object(next(bulk_filename),previous=fbulk)
    except StopIteration:
        print("Ran out of wikipedia related pages.")
    except SizeReached:
        print("Reached the intended size.")
    except KeyboardInterrupt:
        pass
    finally:
        print(f"Final file size: {fdata.tell()} B, {fdata.tell()/float(1<<20)} MB")
        print(f"Number of json docs: {len(processed_titles)}.")
        print(f"Composed in: {(time.time()-start)/60} min")
        fdata.close()
        fbulk.close()

class SizeReached(Exception): pass

def get_related(title):
    with requests.get(api_related.format(urllib.parse.quote_plus(title))) as response:
        response.raise_for_status()
        _data = response.json()["pages"]
        return _data

def get_random():
    response = requests.get(api_random)
    response.raise_for_status()
    _item = response.json()
    return _item

def get_summary(titles):
    _data = list()
    for title in titles:
        response = requests.get(api_summary.format(urllib.parse.quote_plus(title)))
        response.raise_for_status()
        _data.append(response.json())
    return _data

def _run_parallel(max_workers, function, todo_list):
    start = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        _data = list(pool.map(function,todo_list))
    _logger.debug(f"Completed function {function.__name__} on {len(todo_list)} items with {max_workers} workers in: {time.time()-start} s")
    return _data

def _increment_file_object(name, previous, mode="w"):
    _logger.info(f"Rotating file {previous.name} to {name}")
    previous.close()
    return open(name, mode)

def main(**kwargs):
    generate(size=kwargs["size"], initial_titles=kwargs.get("titles",None))

def _parse_args():
    parser = argparse.ArgumentParser(
        description="Get JSON data from wikipedia REST API (summaries) related to specified initial titles up to defined size. Script also prepares chunked files for load to Elasticsearch via _bulk API.",
        epilog=f"Example: python3 wikipedia_api_json_data.py 20971520 --titles Amazon_\(company\) Google Facebook Microsoft")
    parser.add_argument(
        'size', help='Size of raw json data to get (in bytes).', type=int)
    parser.add_argument(
        '--titles', help='Initial titles to which get the related content (space separated). Make sure you specify valid titles.', nargs='+')
    args = parser.parse_args()
    return vars(args)

if __name__ == "__main__":
    sys.exit(main(**_parse_args()))