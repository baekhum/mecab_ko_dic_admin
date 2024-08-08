ARG STACK_VERSION
FROM docker.elastic.co/elasticsearch/elasticsearch:$STACK_VERSION

USER elasticsearch
RUN elasticsearch-plugin install analysis-nori
