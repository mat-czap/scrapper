from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://user:password@0.0.0.0:3306/db'
    db.init_app(app)

    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )

    with app.app_context():
        import scrapper.models
        db.create_all()

        # import pdb; pdb.set_trace()
        # db.create_all()
        # Include our Routes
        from scrapper.server import site
        app.register_blueprint(site)
        return app