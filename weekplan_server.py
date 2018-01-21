# -*- coding: utf-8 -*-
"""The weekplan webserver."""
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Meal, Ingredients, Weekmeals

from flask import session as login_session
import random
import string
import datetime

import json

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

app = Flask(__name__)

APPLICATION_NAME = "Week Plan"

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///nutritionplan.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Get all stored menues from DB


@app.route('/login')
def showLogin():
    """Show the login Screen."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def weekplan():
    """Show the weekplan for the  current week."""
    week_meals = session.query(Weekmeals).all()
    # test = session.query(Meal).filter_by(id=available_menu_ids).one()
    # print test

    return render_template('week_plan.html', week_meals=week_meals)


@app.route('/available_menues')
def available_menues():
    """Show all available menues stored in the DB."""
    available_menues = session.query(Meal).all()
    all_ingredients = session.query(Ingredients).all()
    return render_template('availablemenues.html',
                           available_menues=available_menues,
                           all_ingredients=all_ingredients)


@app.route('/available_menues/<int:menu_id>/ingredients',
           methods=['GET', 'POST'])
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
        print "name: " + request.form['name']
        print "veggie: " + str('veggie' in request.form)
        new_meal = Meal(name=request.form['name'],
                        receipt=request.form['receipt'],
                        portions=request.form['portions'],
                        veggie='veggie' in request.form)
        print "new_meal.receipt: " + new_meal.receipt

        session.add(new_meal)
        session.commit()

        lst_ingrds_index = get_index_list('ingredient', request.form.keys())
        for ingrd_index in lst_ingrds_index:
            igd = Ingredients(name=request.form['ingredient_' + ingrd_index],
                              amount=request.form['amount_' + ingrd_index],
                              amount_type=request.form['amount_type_' +
                              ingrd_index], meal=new_meal)
            session.add(igd)
            session.commit()

        return redirect(url_for('available_menues'))
    else:
        return render_template('new_menu.html')


@app.route('/available_menues/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu(menu_id):
    """Delete dialog for the chosen menu."""
    menu_to_delete = session.query(Meal).filter_by(id=menu_id).one()
    ingredients_to_delete = session.query(Ingredients).filter_by(meal_id=
                                                                 menu_id)
    if request.method == 'POST':
        delete_ingredients(ingredients_to_delete)
        session.delete(menu_to_delete)
        # flash('%s erfolgreich geloescht' % menu_to_delete.name)
        session.commit()
        return redirect(url_for('available_menues'))
    else:
        return render_template('delete_menu.html', menu=menu_to_delete)


@app.route('/available_menues/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu(menu_id):
    """Edit dialog for the chosen menu."""
    menu_to_edit = session.query(Meal).filter_by(id=menu_id).one()
    ingredients_to_edit = session.query(Ingredients).filter_by(meal_id=menu_id)
    lst_ingrds_ids = []
    for igrd in ingredients_to_edit:
        lst_ingrds_ids.append(str(igrd.id))
    print lst_ingrds_ids
    if request.method == 'POST':
        if request.form['name']:
            menu_to_edit.name = request.form['name']
        if request.form['receipt']:
            menu_to_edit.receipt = request.form['receipt']
        if request.form['portions']:
            menu_to_edit.portions = request.form['portions']
        menu_to_edit.veggie = 'veggie' in request.form

        print "request.form.keys(): " + str(request.form.keys())
        ingrds_index_list = get_index_list('ingredient', request.form.keys())
        print "ingrds_index_list: " + str(ingrds_index_list)

        session.add(menu_to_edit)
        session.commit()

        lst_edited_ingrds = list(set(lst_ingrds_ids).intersection(ingrds_index_list))
        for edited_ingrd_index in lst_edited_ingrds:
            ingrd_to_edit = session.query(Ingredients).filter_by(id=int(edited_ingrd_index)).one()
            print "ingrd_to_edit.name alt: " + ingrd_to_edit.name
            if request.form['ingredient_' + edited_ingrd_index]:
                ingrd_to_edit.name = request.form['ingredient_' + edited_ingrd_index]
            if request.form['amount_' + edited_ingrd_index]:
                ingrd_to_edit.amount = request.form['amount_' + edited_ingrd_index]
            if request.form['amount_type_' + edited_ingrd_index]:
                ingrd_to_edit.amount_type = request.form['amount_type_' + edited_ingrd_index]
            print "ingrd_to_edit.name: " + ingrd_to_edit.name
            session.add(ingrd_to_edit)
            session.commit()
        return redirect(url_for('available_menues'))
    else:
        return render_template('edit_menu.html', menu=menu_to_edit,
                               ingredients=ingredients_to_edit)


@app.route('/choose_date', methods=['GET', 'POST'])
def choose_date():
    """Choose the daterange of the weekplan."""
    if request.method == 'POST':
        try:
            session.query(Weekmeals).delete()
            session.commit()
            print "Weekmeals deleted."
        except:
            session.rollback()
        all_meal_ids = []
        all_meals = session.query(Meal).all()
        for meal in all_meals:
            all_meal_ids.append(int(meal.id))
        print "all_meals: " + str(all_meals)
        print "all_meal_ids: " + str(all_meal_ids)
        nbrOfDays = int(request.form['days'])
        print "nbrOfDays: " + str(nbrOfDays)
        for day_in_plan in range(nbrOfDays):
            random_meal_list_item = random.randrange(len(all_meals))
            testMeal = session.query(Meal).filter_by(id=all_meal_ids[random_meal_list_item]).one()
            # meal_id = day_in_plan + 1
            testWeekMeal = Weekmeals(name=testMeal.name,
                                     receipt=testMeal.receipt,
                                     veggie=testMeal.veggie,
                                     portions=testMeal.portions,
                                     meal_date=datetime.date.today())
            session.add(testWeekMeal)
            print "Meal added to Weekmeals"
        session.commit()
        return redirect(url_for('weekplan'))
    return render_template('weekplan_datepicker.html')


def delete_ingredients(lst_ingredients):
    """Delete ingredients in an ingredient list."""
    for ingredient_to_delete in lst_ingredients:
        session.delete(ingredient_to_delete)


def get_index_list(search_string, request_keys):
    """Get list of indices from form."""
    lst_index = []
    lst_ingrds = filter(lambda k: search_string in k, request_keys)
    if len(lst_ingrds) > 0:
        lst_index = [ingrd.replace(search_string + '_', '')
                     for ingrd in lst_ingrds]
    return lst_index


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
