from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from database_setup import Base, Meal, Ingredients

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///nutritionplan.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class Weekmeals(Base):
    """Create Weekmeals Table."""

    __tablename__ = 'weekmeals'
    # Create table columns.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    receipt = Column(String)
    veggie = Column(Boolean)
    portions = Column(Integer)


Weekmeals.__table__.create(session.bind)
