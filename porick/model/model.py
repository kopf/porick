import datetime
from sqlalchemy import Column, Index, String, Text, DateTime, Integer
from sqlalchemy.dialects.mysql import DOUBLE

from porick.model.meta import Base


def now():
    return datetime.datetime.now()

class Quote(Base):
    __tablename__  = 'chirpy_quotes'
    __table_args__ = {'mysql_engine': 'InnoDB',
                      'sqlite_autoincrement': True}
    id           = Column(Integer(10), nullable=False, primary_key=True)
    body         = Column(Text, nullable=False)
    notes        = Column(Text, nullable=True)
    rating       = Column(Integer(11), nullable=False, default=0)
    votes        = Column(Integer(10, unsigned=True), nullable=False, default=0)
    submitted    = Column(DateTime, nullable=False, default=now)
    approved     = Column(Integer(1, unsigned=True), nullable=False, default=0)
    flagged      = Column(Integer(1, unsigned=True), nullable=False, default=1)
    score        = Column(DOUBLE(unsigned=True), nullable=False, default=1)
