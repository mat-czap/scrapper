from flask import Flask, request, Blueprint
from bs4 import BeautifulSoup
import requests
from scrapper.celery_worker import celery

site = Blueprint('site', __name__)


@site.route('/',methods=['POST'])
def get_name():

    name = request.json
    print(name)
    for url in name["urls"]:
        celery.send_task("scrapper.tasks.scrappe_url", (url,))
        # scrappe_url.delay(url)

    return "ok"

