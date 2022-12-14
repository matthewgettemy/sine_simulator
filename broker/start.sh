docker-compose up -d
sleep 8 
docker exec broker kafka-topics --bootstrap-server broker:9092 --create --topic quickstart

