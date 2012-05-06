import datetime
from sqlalchemy import Column, Index, String, Text, DateTime, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import DOUBLE

from porick.model.meta import Base
from porick.settings import TABLES


def now():
    return datetime.datetime.now()


QuoteToTag = Table(TABLES['quote_to_tag'], Base.metadata,
    Column('quote_id', Integer, ForeignKey(TABLES['quotes'] + '.id')),
    Column('tag_id', Integer, ForeignKey(TABLES['tags'] + '.id'))
)


class Quote(Base):
    __tablename__  = TABLES['quotes']
    __table_args__ = {'mysql_engine': 'InnoDB',
                      'sqlite_autoincrement': True}
    id           = Column(Integer, nullable=False, primary_key=True)
    body         = Column(Text, nullable=False)
    notes        = Column(Text, nullable=True)
    rating       = Column(Integer, nullable=False, default=0)
    votes        = Column(Integer, nullable=False, default=0)
    submitted    = Column(DateTime, nullable=False, default=now)
    approved     = Column(Integer, nullable=False, default=0)
    flagged      = Column(Integer, nullable=False, default=0)
    score        = Column(DOUBLE(unsigned=True), nullable=False, default=1)
    tags         = relationship("Tags", secondary=QuoteToTag)


class Tag(Base):
    __tablename__  = TABLES['tags']
    __table_args__ = {'mysql_engine': 'InnoDB',
                      'sqlite_autoincrement': True}
    id = Column(Integer, nullable=False, primary_key=True)
    tag = Column(String(255), nullable=False, primary_key=True)


#class QuoteToTag(Base):
#    __tablename__  = TABLES['quote_to_tag']
#    __table_args__ = {'mysql_engine': 'InnoDB'}
#    quote_id = Column(Integer, ForeignKey(TABLES['quotes'] + '.id'), primary_key=True)
#    tag_id   = Column(Integer, ForeignKey(TABLES['tags'] + '.id'), primary_key=True)


class Account(Base):
    __tablename__  = TABLES['accounts']
    __table_args__ = {'mysql_engine': 'InnoDB',
                      'sqlite_autoincrement': True}
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    level = Column(Integer, nullable=False, default=0)


class Session(Base):
    __tablename__  = TABLES['sessions']
    __table_args__ = {'mysql_engine': 'InnoDB',
                      'sqlite_autoincrement': True}
    id = Column(Integer, nullable=False, primary_key=True)
    expires = Column(Integer, nullable=False, primary_key=True, default=0)
    data = Column(Text, nullable=False) 

