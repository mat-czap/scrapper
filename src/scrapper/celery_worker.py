from scrapper.wsgi import app
from scrapper import make_celery

celery = make_celery(app)
