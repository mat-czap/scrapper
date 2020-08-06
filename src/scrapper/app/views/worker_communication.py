from http import HTTPStatus
from flask import Blueprint

worker = Blueprint('worker', __name__)


@worker.route('/batch', methods=['GET'])
def ready_batch():
    print("batch is already completed")
    return "ok"
