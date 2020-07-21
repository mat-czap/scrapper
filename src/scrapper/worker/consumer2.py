import json
import os
import time


from scrapper import db, rabbit_connection_factory
#
from bs4 import BeautifulSoup
import requests


# from flask import current_app
#
# from scrapper.models import Link
# from scrapper.wsgi import app

class StatusCode500Error(Exception):
    pass


def scrappe_url(url):
    url = url.decode("utf-8")

    if "http://" not in url:
        url = "http://" + url
    try:
        content = requests.get(url)

        if content.status_code >= 500:
            raise StatusCode500Error

    except StatusCode500Error as exc:
        print("500 error")

    soup = BeautifulSoup(content.text, 'html.parser')

    with open('scrapped_records.txt', 'a') as file:
        for link in soup.find_all('a'):
            file.write(str(link.get('href')) + '\n')


config_location = os.environ.get("CONFIG_SRC")

with open(config_location) as config_file:
    config = json.load(config_file)


connection = rabbit_connection_factory(config.get("RABBITMQ_URL"))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name, routing_key="fo.*")

# channel.queue_declare(queue='hello', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    time.sleep(40)
    scrappe_url(body)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()

#         # new_link = Link(page=url, link=link.get('href'))
#         # db.session.add(new_link)
#         # db.session.commit()
#
