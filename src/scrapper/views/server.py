from http import HTTPStatus

import pika
from flask import request, Blueprint, current_app

from scrapper import rabbit_context
from scrapper.tasks import print_tasks

site = Blueprint('site', __name__)

@site.route('/',methods=['POST'])
def get_name():
    # from scrapper.tasks import scrappe_url
    payload = request.json
    # print(name)
    connection = rabbit_context(current_app.config)
    channel = connection.channel()

    for url in payload["urls"]:
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=url)
        print(" [x] Sent %r" % url)

    return "ok", HTTPStatus.ACCEPTED





