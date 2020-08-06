# scrapper
docker-compose[Flask service + rabbitmq + SqlAlchemy ORM for Mysql]

# Start
docker-compose up

# Curl for testing
curl -v -X POST -H "Content-Type: application/json" -d '{"urls":["example.com"]}' localhost:5001/

# Original concept
![Alt text](schema.jpg?raw=true "schma")
