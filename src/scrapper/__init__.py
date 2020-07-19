from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

from scrapper.rabbitFactory import rabbit_connection_factory

from scrapper.views.health import health
import pika

db = SQLAlchemy()
metrics = PrometheusMetrics(app=None)

def create_app():
    """Initialize the core application."""

    app = Flask(__name__, instance_relative_config=False)

    db.init_app(app)
    metrics.init_app(app)
    metrics.info('app_info', 'Application info', version='1.0.3')
    app.config.from_envvar('APP_MODE')

    print(app.config.get("RABBITMQ_URL"))

    connection = rabbit_connection_factory(app.config.get("RABBITMQ_URL"))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='topic')
    # channel.queue_declare(queue='hello', durable=True)


    with app.app_context():
        import scrapper.models
        db.create_all()
        # Include our Routes
        from scrapper.views.server import site
        app.register_blueprint(site)
        app.register_blueprint(health)

        return app