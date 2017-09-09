# -*- coding: utf-8 -*-
"""Initial meal database population"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Meal, Ingredients

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# The Database Engine
engine = create_engine('sqlite:///nutritionplan.db')
# Bind the engine to the Bases's metadata
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Meal Low Carb Pizzarole
meal1 = Meal(name="Low Carb Pizzarolle", receipt="Den Backofen auf 170 C"
             "vorheizen. Fuer den Boden Quark, Eier und 120 g Kaese in einer"
             "Schuessel miteinander verruehren und wuerzen. Die Masse auf das mit"
             "Backpapier ausgelegte Backblech kippen und glatt streichen."
             "15 Minuten im Ofen backen. Das Backblech herausnehmen und den"
             "Boden beliebig belegen mit z. B. Tomatensauce, Salami, Schinken,"
             "Zucchini, Champignons oder Mais. Mit dem restlichen Kaese"
             "bestreuen und erneut in den Ofen schieben, bis der Kaese eine"
             "schoene Farbe hat. Abkuehlen lassen, mit Rucola bestreuen und"
             "vorsichtig einrollen. Eingerollt in Alufolie mehrere Tage im"
             "Kuehlschrank haltbar.",
             veggie=True, portions=3)

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

ingredient4 = Ingredients(name="Gemuese", meal=meal1)

session.add(ingredient3)
session.commit()

#
meal2 = Meal(name="Gnocchi-Salat mit Pinienkernen", receipt="Die Gnocchi nach"
             "Anleitung zubereiten und abkuehlen lassen.", veggie=True,
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
