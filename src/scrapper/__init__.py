from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from scrapper.views.health import health


db = SQLAlchemy()
metrics = PrometheusMetrics(app=None)

def create_app():
    """Initialize the core application."""

    app = Flask(__name__, instance_relative_config=False)

    db.init_app(app)
    metrics.init_app(app)
    metrics.info('app_info', 'Application info', version='1.0.3')
    app.config.from_envvar('APP_MODE')
    app.config.update(
        CELERY_BROKER_URL='redis://scrapper_redis_1:6379/0',
        CELERY_RESULT_BACKEND='redis://scrapper_redis_1:6379/0',
    )

    with app.app_context():
        import scrapper.models
        db.create_all()

        # Include our Routes
        from scrapper.views.server import site
        app.register_blueprint(site)
        app.register_blueprint(health)
        return app