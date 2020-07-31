from http import HTTPStatus

from flask import Blueprint

worker = Blueprint('worker', __name__)


@worker.route('/batch', methods=['GET'])
def ready_batch():
    print("ok,thx for msg batch is already completed")
    return HTTPStatus.OK
