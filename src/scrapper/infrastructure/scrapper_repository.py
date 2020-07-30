import sqlalchemy as db
from sqlalchemy import orm

from scrapper.infrastructure.models import Batch


class ScrapperRepository:

    def __init__(self, mySql_connection : str):
        engine = db.create_engine(mySql_connection)
        self._session = orm.scoped_session(orm.sessionmaker())(bind=engine)

    def create_batch(self):
        batch = Batch()
        print(batch)
        self._session.add(batch)
        self._session.commit()