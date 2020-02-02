#!/bin/bash
curl --request PUT 'http://localhost:9200/test-norms-freqs' \
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
                        "type": "text",
                        "norms": false,
                        "index_options": "freqs",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    }
                }
            }
        ]
    }
}'