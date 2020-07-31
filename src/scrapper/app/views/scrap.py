from http import HTTPStatus
import pickle

import pika
from flask import request, Blueprint, current_app

from scrapper.app.packager import Packager
from scrapper.infrastructure import rabbit_connection_factory
from scrapper.infrastructure.scrapper_repository import ScrapperRepository

site = Blueprint('site', __name__)


@site.route('/', methods=['POST'])
def get_name():
    # from scrapper.tasks import scrappe_url
    payload = request.json
    connection = rabbit_connection_factory(current_app.config.get("RABBITMQ_URL"))
    repository = ScrapperRepository(current_app.config["SQLALCHEMY_DATABASE_URI"])
    batch_id = repository.create_batch()
    packager = Packager(payload)
    channel = connection.channel()

    # todo put logic to another file
    # topic type
    for url in payload["urls"]:
        var = str()
        try:
            if url[-2:] == "pl":
                var = "pl."
            if url[-2:] != "pl":
                var = "fo."
            if len(url) >= 20:
                var += "long"
            else:
                var += "short"
        except Exception as ex:
            print(ex)

        # Logic to send signal about last element

        package = [url, batch_id,len(payload)]

        channel.basic_publish(exchange='logs',
                              routing_key=f"{var}",
                              body=pickle.dumps(package))

    return "ok", HTTPStatus.ACCEPTED
