from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://user:password@0.0.0.0:3306/db'
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {'pool_recycle': 499, 'pool_timeout': 10, 'pool_pre_ping': True}
    # app.config['SQLALCHEMY_POOL_RECYCLE'] = 499
    # app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
    db.init_app(app)

    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    )

    with app.app_context():
        import scrapper.models
        db.create_all()

        # Include our Routes
        from scrapper.server import site
        app.register_blueprint(site)
        return app