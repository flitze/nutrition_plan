# -*- coding: utf-8 -*-
"""Create Database for a weekly nutrition plan."""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """Create User Table."""

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    

class Meal(Base):
    """Create Meal Table."""

    __tablename__ = 'meal'
    # Create table columns.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    receipt = Column(String)
    veggie = Column(Boolean)
    portions = Column(Integer)

    @property
    def serialize(self):
        """Serialize meal database entry."""
        return {
            'meal_name': self.name,
            'receipt': self.receipt,
            'veggie': self.veggie,
            'portions': self.portions,
            'id': self.id
        }

    def get_meal_name(self):
        return self.name


class Ingredients(Base):
    """Create Ingredients Table."""

    __tablename__ = 'ingredients'
    # Create table columns.
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    amount_type = Column(String(80))
    meal_id = Column(Integer, ForeignKey('meal.id'))
    meal = relationship(Meal)

    @property
    def serialize(self):
        """Serialze ingredients database entry."""
        return {
            'name': self.name,
            'amount': self.amount,
            'amount_type': self.amount_type,
            'meal_id': self.meal_id,
            'ingredient_id': self.ingredient_id
        }


# Create database file.
engine = create_engine('sqlite:///nutritionplan.db')
Base.metadata.create_all(engine)
