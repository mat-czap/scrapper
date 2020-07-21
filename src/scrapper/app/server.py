from flask import Flask

from prometheus_flask_exporter import PrometheusMetrics

from scrapper.infrastructure.rabbitFactory import rabbit_connection_factory




metrics = PrometheusMetrics(app=None)

def create_app():
    """Initialize the core application."""

    app = Flask(__name__, instance_relative_config=False)


    metrics.init_app(app)
    metrics.info('app_info', 'Application info', version='1.0.3')
    app.config.from_envvar('APP_MODE')

    print(app.config)

    connection = rabbit_connection_factory(app.config.get("RABBITMQ_URL"))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='topic')
    # channel.queue_declare(queue='hello', durable=True)


    with app.app_context():
        import scrapper.infrastructure.models

        # Include our Routes
        from scrapper.app.views import site, health
        app.register_blueprint(site)
        app.register_blueprint(health)
        return app