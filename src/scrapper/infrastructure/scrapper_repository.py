import sqlalchemy as db
from sqlalchemy import orm

from scrapper.infrastructure.models import Batch, Link, Status


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

    def add_link(self, page, link, batch_id) -> None:
        new_link = Link(link=link, page=page, batch_id=batch_id)
        self._session.add(new_link)
        self._session.commit()

    def update_batch_finished(self, batch_id):
        self._session.query(Batch).filter_by(id=batch_id).first().update({'status':Status.FINISHED})
        self._session.commit()

