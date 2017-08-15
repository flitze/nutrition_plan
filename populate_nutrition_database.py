
"""Initial meal database population"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Meal, Ingredients

# The Database Engine
engine = create_engine('sqlite:///nutritionplan.db')
# Bind the engine to the Bases's metadata
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Meal Low Carb Pizzarole
meal1 = Meal(name="Low Carb Pizzarolle", receipt="Fuer den Boden Quark",
             type="vegetarisch", portions=3)

session.add(meal1)
session.commit()

ingredient1 = Ingredients(name="Quark", amount=120, amount_type="weight",
                          meal=meal1)

session.add(ingredient1)
session.commit
