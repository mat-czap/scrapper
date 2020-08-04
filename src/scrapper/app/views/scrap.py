from http import HTTPStatus
from flask import request, Blueprint, current_app

from scrapper.app.packager import Packager
from scrapper.infrastructure import rabbit_connection_factory
from scrapper.infrastructure.scrapper_repository import ScrapperRepository

site = Blueprint('site', __name__)


@site.route('/', methods=['POST'])
def get_name():
    connection = rabbit_connection_factory(current_app.config["RABBITMQ_URL"])
    repository = ScrapperRepository(current_app.config["SQLALCHEMY_DATABASE_URI"])
    channel = connection.channel()
    batch_id = repository.create_batch()
    payload = request.json
    packager = Packager(payload)

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

        channel.basic_publish(exchange='logs',
                              routing_key=f"{var}",
                              body=packager.send(url, batch_id))
    return "ok", HTTPStatus.ACCEPTED
