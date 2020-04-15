from bs4 import BeautifulSoup
import requests
from scrapper.models import Link
from scrapper import db
from celery import Celery
from scrapper.wsgi import app

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


celery_app = make_celery(app)


# app = Celery('tasks', broker='redis://localhost:6379/0')
class StatusCode500Error(Exception):
    pass


@celery_app.task(bind=True)
def scrappe_url(self, url):

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

