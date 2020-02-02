#!/bin/bash
for i in $1/*.bulk; do curl --location --request POST "http://localhost:9200/$2/_doc/_bulk?refresh=true" --header 'Content-Type: application/x-ndjson' --data-binary "@$i"; done