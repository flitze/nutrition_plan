"""The weekplan webserver."""
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Meal, Ingredients

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

app = Flask(__name__)

engine = create_engine('sqlite:///nutritionplan.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def weekplan():
    """Show the weekplan for the  current week."""
    week_menues = session.query(Meal).all()
    menu_names = " "
    for menu in week_menues:
        menu_names += menu.name
        menu_names += "</br>"
    return menu_names


@app.route('/available_menues')
def available_menues():
    """Show all available menues stored in the DB."""
    available_menues = session.query(Meal).all()
    return render_template('availablemenues.html',
                           available_menues=available_menues)


@app.route('/available_menues/<int:menu_id>/ingredients')
def ingredients(menu_id):
    """Show all ingredients for a specific menu."""
    clicked_menu = session.query(Meal).filter_by(id=menu_id).one()
    print "clicked_menu: " + str(clicked_menu)
    menu_ingredients = session.query(Ingredients).filter_by(meal_id=menu_id)
    return render_template('ingredients.html', menu=clicked_menu,
                           ingredients=menu_ingredients)


@app.route('/available_menues/new', methods=['GET', 'POST'])
def add_new_meal():
    """Add a new meal to the available menues list."""
    if request.method == 'POST':
        print "name: " + str(request.form['name'])
        print "veggie: " + str('veggie' in request.form)
        newMeal = Meal(name=request.form['name'],
                       receipt=request.form['receipt'],
                       portions=request.form['portions'],
                       veggie='veggie' in request.form)
        session.add(newMeal)
        session.commit()
        return redirect(url_for('available_menues'))
    else:
        return render_template('new_menu.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
