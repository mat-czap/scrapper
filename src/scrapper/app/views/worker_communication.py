import requests
from flask import Blueprint, request

worker = Blueprint('worker', __name__)


@worker.route('/batch', methods=['POST'])
def ready_batch():
    content = request.json
    batch_id = content["batch_id"]
    print(f'batch nr. {batch_id} is already completed')
    return "ok"
