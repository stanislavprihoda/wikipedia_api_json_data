#!/bin/bash
curl localhost:9200/_cat/shards/elastic-storage*?v
curl localhost:9200/elastic-storage-test/_ilm/explain?pretty
