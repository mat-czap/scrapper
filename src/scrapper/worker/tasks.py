import json
import os
import pickle
import time

import requests
from bs4 import BeautifulSoup

from scrapper.infrastructure import rabbit_connection_factory
from scrapper.infrastructure.scrapper_repository import ScrapperRepository
from scrapper.worker.Worker import Worker


class StatusCode500Error(Exception):
    pass


def scrap_by_url(package):
    url, batch_id = package
    print(url, batch_id)

    # if "http://" not in url:
    #     url = "http://" + url

    content = str()
    try:
        content = requests.get(url)

        if content.status_code >= 500:
            raise StatusCode500Error

    except StatusCode500Error as exc:
        print("500 error")

    soup = BeautifulSoup(content.text, 'html.parser')

    def input_to_db(link):
        link if link is None else link.encode('utf-8')

    for link in soup.find_all('a'):
        repository = ScrapperRepository(config["SQLALCHEMY_DATABASE_URI"])
        repository.add_link(url, input_to_db(link.get('href')), batch_id)

# todo put config to separate file
config_location = os.environ.get("APP_MODE")

with open(config_location) as config_file:
    config = json.loads(*config_file.readlines())

# with open(config_location, mode="rb") as config_file:
#     exec(compile(config_file.read(), config_location, "exec"), config)

connection = rabbit_connection_factory(config.get("RABBITMQ_URL"))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name, routing_key="#")

# channel.queue_declare(queue='hello', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


repository = ScrapperRepository(config["SQLALCHEMY_DATABASE_URI"])


def scrap_job(body, repository):

    worker = Worker(body, repository)
    scrapped_links = scrap_by_url(Worker.get_params_to_scrap)

    if scrapped_links["status"] == "ok":
        worker.commit(scrapped_links)
    else:
        return "Worker failed scrapping"


def callback(ch, method, properties, body):
    time.sleep(1)
    scrap_job(body, repository)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
