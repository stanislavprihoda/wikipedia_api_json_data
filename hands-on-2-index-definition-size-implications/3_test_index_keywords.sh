#!/bin/bash
curl --request PUT 'http://localhost:9200/test-keywords' \
--header 'Content-Type: application/json' \
-d '{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "dynamic_templates": [
            {
                "strings": {
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            }
        ]
    }
}'