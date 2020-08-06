# Scrapper
main tools:
- Flask
- Rabbitmq
- SqlAlchemy
- Mysql
- Gunicorn
- Docker-compose

# Start
docker-compose up

# Curl for testing
curl -v -X POST -H "Content-Type: application/json" -d '{"urls":["example.com"]}' localhost:5001/

# Original concept
![Alt text](schema.jpg?raw=true "schma")
