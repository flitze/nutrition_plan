"""The weekplan webserver."""
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Meal, Ingredients

app = Flask(__name__)

engine = create_engine('sqlite:///nutritionplan.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def weekplan():
    return "Server works"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
