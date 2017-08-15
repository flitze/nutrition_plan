"""Create Database for a weekly nutrition plan"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Meal(Base):
    """Create Meal Table."""

    __tablename__ = 'meal'
    # Create table columns.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    receipt = Column(String)
    type = Column(String(80))


class Ingredients(Base):
    """Create Ingredients Table."""

    __tablename__ = 'ingredients'
    # Create table columns.
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    amount_type = Column(String(80))
    portions = Column(Integer)
    meal_id = Column(Integer, ForeignKey('meal.id'))
    meal = relationship(Meal)


# Create database file.
engine = create_engine('sqlite:///nutritionplan.db')
Base.metadata.create_all(engine)
