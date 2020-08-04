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


def scrap_by_url(url):
    if "http://" not in url:
        url = "http://" + url

    content = str()

    try:
        content = requests.get(str(url))
        if content.status_code >= 500:
            raise StatusCode500Error

    except StatusCode500Error as exc:
        print("500 error")

    soup = BeautifulSoup(content.text, 'html.parser')

    def input_acceptable_by_db(link):
        "" if link is None else link.encode('utf-8')

    scrapped_links = dict()
    links = set()

    try:
        for link in soup.find_all('a'):
            if link is not None:
                links.add(link.get('href'))
            else:
                continue

        scrapped_links['data'] = links
        scrapped_links['status'] = "ok"
    except Exception as ex:
        print(ex)
    return scrapped_links

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


worker = Worker(repository)



def scrap_job(worker, body):
    print(pickle.loads(body))
    time.sleep(2)
    worker.set_data_from_queue(body)
    scrapping_input = worker.get_params_to_scrap()
    try:
        scrapped_links = scrap_by_url(scrapping_input)
    except Exception as ex:
        print("scrappJOB",ex)

    if scrapped_links["status"] == "ok":
        worker.commit(scrapped_links)
    else:
        return "Worker failed scrapping"








def callback(ch, method, properties, body):
    time.sleep(5)
    scrap_job(worker, body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
