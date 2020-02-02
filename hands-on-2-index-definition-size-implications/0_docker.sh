#!/bin/bash
docker network create elastic-network
docker run --rm --detach --name elastic -p 9200:9200 --network elastic-network -e "node.name=elastic" -e "discovery.type=single-node" -e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1 -e ES_JAVA_OPTS="-Xms2g -Xmx2g" docker.elastic.co/elasticsearch/elasticsearch:7.5.1
docker run --rm --detach --link elastic:elasticsearch --name kibana --network elastic-network -p 5601:5601 docker.elastic.co/kibana/kibana:7.5.1
docker ps
