from flask import Flask, request, Blueprint
from bs4 import BeautifulSoup
import requests

site = Blueprint('site', __name__)

@site.route('/',methods=['POST'])
def get_name():
    from scrapper.datebase import db
    from scrapper.models import Link

    name = request.json
    print(name)
    for url in name["urls"]:
        content = requests.get(url)
        print(content)
        soup = BeautifulSoup(content.text, 'html.parser')
        for link in soup.find_all('a'):
            new_link = Link(page=url, link= link.get('href'))
            db.session.add(new_link)
            db.session.commit()



    return "ok"

