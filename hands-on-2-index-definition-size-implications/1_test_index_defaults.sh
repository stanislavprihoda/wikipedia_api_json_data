#!/bin/bash
curl --request PUT 'http://localhost:9200/test-defaults' \
--header 'Content-Type: application/json' \
-d '{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}'