import pytest

from scrapper import db
from scrapper import app


@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()
