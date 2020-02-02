#!/bin/bash
curl --location --request PUT 'http://localhost:9200/_ilm/policy/elastic_storage_policy' \
--header 'Content-Type: application/json' \
--data-raw '{
    "policy": {
        "phases": {
            "warm": {
                "min_age": "1m",
                "actions": {
                    "allocate": {
                        "require": {
                            "type": "warm"
                        }
                    }
                }
            }
        }
    }
}'
