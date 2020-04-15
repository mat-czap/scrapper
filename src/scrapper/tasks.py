from bs4 import BeautifulSoup
import requests
from celery import Celery
from scrapper.celery_worker import celery
from scrapper.models import Link
from scrapper import db
from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery



# app = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def scrappe_url(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    for link in soup.find_all('a'):
        new_link = Link(page=url, link=link.get('href'))

        db.session.add(new_link)
        db.session.commit()

