from enum import Enum
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class StatusPackage(Enum):
    STARTED = 0
    FINISHED = 1


class Batch(base):

    __tablename__ = "batch"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(StatusPackage), default=StatusPackage.STARTED)
    links = relationship("Link", back_populates="batch")

    def __repr__(self):
        return f"batch: {self.id}"


class Link(base):

    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(2000), default='none')
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'))
    batch = relationship("Batch", back_populates="links")

    def __repr__(self):
        return f"link: {self.link}"