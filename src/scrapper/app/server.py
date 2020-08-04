from flask import Flask
import sqlalchemy as db
from sqlalchemy import orm
from scrapper.infrastructure.models import base
from prometheus_flask_exporter import PrometheusMetrics
from scrapper.infrastructure.rabbitFactory import rabbit_connection_factory

metrics = PrometheusMetrics(app=None)


def create_app():
    """Initialize the core application."""

    app = Flask(__name__, instance_relative_config=False)

    metrics.init_app(app)
    metrics.info('app_info', 'Application info', version='1.0.3')
    app.config.from_envvar('APP_MODE')

    connection = rabbit_connection_factory(app.config.get("RABBITMQ_URL"))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='topic')

    engine = db.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    base.metadata.bind = engine
    session = orm.scoped_session(orm.sessionmaker())(bind=engine)
    base.metadata.create_all()

    with app.app_context():
        from scrapper.app.views import site, health, worker
        app.register_blueprint(site)
        app.register_blueprint(health)
        app.register_blueprint(worker)
        return app
