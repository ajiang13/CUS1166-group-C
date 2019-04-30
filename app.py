#Imports
from flask import Flask, render_template, url_for, request, redirect, flash, session
import json
import db
import sqlite3
from tables import Results
from forms import SearchForm, AdvancedSearchForm, FilterForm, RestaurantForm, RegistrationForm, LoginForm
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_args
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

# Create an instance of Flask class
app = Flask(__name__, template_folder='templates')
bootstrap = Bootstrap(app)
app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/rsmal188/Documents/CUS1166-group-c-dev-small/database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    username = db. Column(db.String(120), unique=True, nullable=False)
    email = db. Column(db.String(60), unique=True, nullable=False)
    password = db. Column(db.String(60), nullable=False)

#Routes
@app.route("/")
def index():
    return render_template('index.html')

#Search
@app.route("/search", methods=['GET', 'POST'])
def search():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('search.html', form=search)

@app.route("/search_results/page/<int:page>", methods=['GET', 'POST'])
@app.route("/search_results", defaults={'page': 1}, methods=['GET', 'POST'])
def search_results(advanced_search, form, page):
    results = []
    filter = FilterForm(request.form)
    if advanced_search.data['name'] != '' or advanced_search.data['city'] != '' or advanced_search.data['state'] != '' or advanced_search.data['categories'] != '' or advanced_search.data['stars'] != '':
        q1 = advanced_search.data['name']
        q2 = advanced_search.data['city']
        q3 = advanced_search.data['state']
        q4 = advanced_search.data['categories']
        q5 = advanced_search.data['stars']
        #Creating sessions to pass into search_results_filtered
        session['adv_search_name'] = q1
        session['adv_search_city'] = q2
        session['adv_search_state'] = q3
        session['adv_search_categories'] = q4
        session['adv_search_stars'] = q5
        results, result_count = db.advanced_search(q1, q2, q3, q4, q5)
        total = result_count
        page = request.args.get('page', '1')
        page = int(page)
        per_page = 20
        offset = (page - 1) * per_page
        results_for_render = results.skip(offset).limit(per_page)
        pagination = Pagination(page=page, per_page=per_page, offset=offset, total=total, format_total=True, format_number=True, css_framework='bootstrap4')
    if not results:
        flash('No results found')
        return redirect('/search')
    else:
        return render_template('search_results.html', form=form, filterform=filter, results=results, result_count=result_count, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, page=page, per_page=per_page, pagination=pagination)

@app.route("/search_results_filtered", methods=['GET', 'POST'])
def search_results_filtered():
    results = []
    filter = FilterForm(request.form)

    if session['adv_search_name'] != '' or session['adv_search_city'] != '' or session['adv_search_state'] != '' or session['adv_search_categories'] != '' or session['adv_search_stars'] != '':
        q1 = session['adv_search_name']
        q2 = session['adv_search_city']
        q3 = session['adv_search_state']
        q4 = session['adv_search_categories']
        q5 = session['adv_search_stars']

        results, result_count = db.advanced_search(q1, q2, q3, q4, q5)
        total = result_count
        page = request.args.get('page', '1')
        page = int(page)
        per_page = 20
        offset = (page - 1) * per_page
        results_for_render = results.skip(offset).limit(per_page)
        pagination = Pagination(page=page, per_page=per_page, offset=offset, total=total, format_total=True, format_number=True, css_framework='bootstrap4')
    if not results:
        flash('No results found')
        return redirect('/search')
    if request.form.get('sortbutton') == "Sort Ascending":
        sortby = filter.data['select']
        sortedresults = db.sort_request(sortby,results,1)
        return render_template('search_results.html', filterform = filter, results=sortedresults, result_count=result_count, page=page, per_page=per_page, pagination=pagination)
    else:
        sortby = filter.data['select']
        sortedresults = db.sort_request(sortby,results,-1)
        #sortedresults = db.filter_by_stars(results, 3)
        return render_template('search_results.html', filterform = filter, results=sortedresults, result_count=result_count, page=page, per_page=per_page, pagination=pagination)

@app.route('/new_restaurant', methods=['GET', 'POST'])
def new_restaurant():
    """
    Add a new restaurant
    """
    form = RestaurantForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the restaurant
        restaurant = Restaurant()
        save_changes(restaurant, form, new=True)
        flash('Restaurant created successfully!')
        return redirect('/')
    return render_template('new_restaurant.html', form=form)

#Edit
@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):

    qry = db.query(Restaurant).filter(Restaurant).id==id
    restaurant = qry.first()

    if restaurant:
        form = RestaurantForm(formdata=request.form, obj=restaurant)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(restaurant, form)
            flash('Restaurant updated successfully!')
            return redirect('/')
        return render_template('edit_restaurant.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = user.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        try:
            form = request.form
            registered_user = user(form["name"],form["username"], form["emaiil"], form["password"])
            db.session.add(registered_user)
            db.session.commit

        except:
            return render_template('register.html', form=form)
    return render_template('register.html', error="There was an error registering this user")

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)
