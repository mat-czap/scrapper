from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from scrapper.views.health import health
import pika

from flask.ext.pika import Pika as FPika



db = SQLAlchemy()
metrics = PrometheusMetrics(app=None)

def create_app():
    """Initialize the core application."""

    app = Flask(__name__, instance_relative_config=False)

    db.init_app(app)
    metrics.init_app(app)
    metrics.info('app_info', 'Application info', version='1.0.3')
    app.config.from_envvar('APP_MODE')
    print(app.config['RABBITMQ_URL'])

    fpika = Fpika()
    fpika.init_app(app)

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')


    with app.app_context():
        import scrapper.models
        db.create_all()

        # Include our Routes
        from scrapper.views.server import site
        app.register_blueprint(site)
        app.register_blueprint(health)

        return app