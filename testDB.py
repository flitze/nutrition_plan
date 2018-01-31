from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from database_setup import Base, Meal, Ingredients, Weekmeals

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///nutritionplan.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

'''
class Weekmeals(Base):
    """Create Weekmeals Table."""

    __tablename__ = 'weekmeals'
    __table_args__ = {'extend_existing': True}
    # Create table columns.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    meal_date = Column(Date)
    receipt = Column(String)
    veggie = Column(Boolean)
    portions = Column(Integer)
'''

# Weekmeals.__table__.drop(session.bind)
# Weekmeals.__table__.create(session.bind)


class Week_Ingredients(Base):
    """Create Weekmeal Ingredients Table."""

    __tablename__ = 'week_ingredients'
    __table_args__ = {'extend_existing': True}
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    amount_type = Column(String(80))
    meal_id = Column(Integer, ForeignKey('meal.id'))
    meal = relationship(Meal)
    weekmeal_id = Column(Integer, ForeignKey('weekmeals.id'))
    weekmeals = relationship(Weekmeals)

Week_Ingredients.__table__.drop(session.bind)
Week_Ingredients.__table__.create(session.bind)
