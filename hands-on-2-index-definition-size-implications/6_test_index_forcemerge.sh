#!/bin/bash
curl --request POST 'http://localhost:9200/test-*/_forcemerge?max_num_segments=1' 
