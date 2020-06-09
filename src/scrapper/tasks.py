from bs4 import BeautifulSoup
import requests
from scrapper.models import Link
from scrapper import db
from celery import Celery
from scrapper.wsgi import app



# app = Celery('tasks', broker='redis://localhost:6379/0')
class StatusCode500Error(Exception):
    pass



def scrappe_url(self, url):
    if "http://" not in url:
        url="http://"+url

    try:
        content = requests.get(url)

        if content.status_code >= 500:
            raise StatusCode500Error

    except StatusCode500Error as exc:
        print("500 error")
        raise self.retry(exc=exc)

    except Exception as exc:
        raise self.retry(exc=exc)

    soup = BeautifulSoup(content.text, 'html.parser')
    for link in soup.find_all('a'):
        new_link = Link(page=url, link=link.get('href'))
        db.session.add(new_link)
        db.session.commit()

