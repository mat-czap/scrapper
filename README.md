# scrapper
Flask service for scrapping + docker-compose + rabbitmq + Mysql/Redis + Prometheus/Grafana


curl for testing:
curl -v -X POST -H "Content-Type: application/json" -d '{"urls":["http://www.wp.pl","http://www.onet.pl","http://www.interia.pl","http://www.allegro.pl","http://www.guardian.co.uk"]}' localhost:5001/

#Origin concept
![Alt text](schema.jpg?raw=true "schma")