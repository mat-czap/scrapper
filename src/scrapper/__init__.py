from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://user:password@0.0.0.0:3306/db'
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Include our Routes
        from scrapper.server import site
        app.register_blueprint(site)
        return app