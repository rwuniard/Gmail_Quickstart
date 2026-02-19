docker pull apache/activemq-artemis
docker run -d --name activemq-artemis \
  -p 5672:5672 \
  -p 8161:8161 \
  apache/activemq-artemis