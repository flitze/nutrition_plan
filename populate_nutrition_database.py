
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
session.commit()

ingredient2 = Ingredients(name="Eier", amount=3, amount_type="pieces",
                          meal=meal1)

session.add(ingredient2)
session.commit()

ingredient3 = Ingredients(name="Kaese", amount=240, amount_type="weight",
                          meal=meal1)

session.add(ingredient3)
session.commit()

#
meal2 = Meal(name="Gnocchi-Salat mit Pinienkernen", receipt="Die Gnocchi nach"
             "Anleitung zubereiten und abkuehlen lassen.", type="vegetarisch",
             portions=4)

session.add(meal2)
session.commit()

ingredient1 = Ingredients(name="Gnocchi", amount=800, amount_type="weight",
                          meal=meal2)

session.add(ingredient1)
session.commit()

ingredient2 = Ingredients(name="Pinienkerne", amount=50, amount_type="weight",
                          meal=meal2)

session.add(ingredient2)
session.commit()
