#!/bin/bash
curl --location --request DELETE 'http://localhost:9200/elastic-storage-test*'
curl --location --request DELETE 'http://localhost:9200/_template/elastic-storage-test*'