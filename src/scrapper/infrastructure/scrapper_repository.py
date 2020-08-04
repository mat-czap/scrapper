import sqlalchemy as db
from sqlalchemy import orm
from scrapper.infrastructure.models import Batch, Link, StatusPackage


class ScrapperRepository:

    def __init__(self, mysql_connection: str):
        engine = db.create_engine(mysql_connection)
        self._session = orm.scoped_session(orm.sessionmaker())(bind=engine)

    def create_batch(self) -> int:
        batch = Batch()
        self._session.add(batch)
        self._session.flush()
        self._session.commit()
        return batch.id

    def add_link(self, page: str, link: str, batch_id: int):
        new_link = Link(link=link, page=page, batch_id=batch_id)
        self._session.add(new_link)
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            self._session.flush()
            raise Exception

    def update_batch_status(self, batch_id: int):
        retrieved_batch = self._session.query(Batch).filter(Batch.id == batch_id).first()
        retrieved_batch.status = StatusPackage.FINISHED
        self._session.commit()
