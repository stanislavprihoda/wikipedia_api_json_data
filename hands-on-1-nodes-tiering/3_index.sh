#!/bin/bash
curl --location --request PUT 'http://localhost:9200/elastic-storage-test' \
--header 'Content-Type: application/json' \
--data-raw '{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "index.lifecycle.name": "elastic_storage_policy",
        "index.routing.allocation.require.type": "hot"
    }
}'