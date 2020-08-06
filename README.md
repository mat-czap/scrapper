# scrapper
Flask service for scrapping + docker-compose + rabbitmq + Mysql/Redis + Prometheus/Grafana


curl for testing:
curl -v -X POST -H "Content-Type: application/json" -d '{"urls":["example.com"]}' localhost:5001/

#original concept
![Alt text](schema.jpg?raw=true "schma")
