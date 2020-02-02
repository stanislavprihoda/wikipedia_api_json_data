#!/bin/bash
curl --location --request PUT 'http://localhost:9200/_cluster/settings' \
--header 'Content-Type: application/json' \
--data-raw '{
    "transient": {
        "indices.lifecycle.poll_interval": "1m"
    }
}'