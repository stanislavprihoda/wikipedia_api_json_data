#!/bin/bash
curl --location --request PUT 'http://localhost:9200/elastic-storage-test/_settings' \
--header 'Content-Type: application/json' \
--data-raw '{
  "index.routing.allocation.require.type": "warm"
}'