from http import HTTPStatus

import pika
from flask import request, Blueprint, current_app, app

from scrapper import rabbit_connection_factory

site = Blueprint('site', __name__)


@site.route('/', methods=['POST'])
def get_name():
    # from scrapper.tasks import scrappe_url
    payload = request.json
    connection = rabbit_connection_factory(current_app.config.get("RABBITMQ_URL"))
    print(current_app.config)
    channel = connection.channel()

    # direct type:
    # for key, url in enumerate(payload["urls"], 1):
    #     var = str()
    #     if key % 2 == 1:
    #         var = 'a'
    #     else:
    #         var = "b"
    #     channel.basic_publish(exchange='logs',
    #                           routing_key=f"{var}",
    #                           body=url)
    #     print(" [x] Sent %r" % url)

    # topic type
    for url in payload["urls"]:
        var = str()
        if url[-2:] == "pl":
            var = "pl."
        if url[-2:] != "pl":
            var = "fo."
        if len(url) >= 20:
            var += "long"
        else:
            var += "short"
        channel.basic_publish(exchange='logs',
                              routing_key=f"{var}",
                              body=url)
        print(" [x] Sent %s with routing_key %s" % (url, var))
    return "ok", HTTPStatus.ACCEPTED
