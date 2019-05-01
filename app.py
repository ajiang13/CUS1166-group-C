# Imports
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import os

from config import Config
from flask import (Flask, render_template, url_for, request, redirect, flash,
                   session)
from flask_bootstrap import Bootstrap
from flask_login import login_user
from flask_mail import Mail, Message
from flask_paginate import Pagination, get_page_args
from flask_sqlalchemy import SQLAlchemy
from forms import (AdvancedSearchForm, FilterForm, RestaurantForm, MailForm,
                   DisplayForm, RegistrationForm)
from flask_s3 import FlaskS3
import db

# Create an instance of Flask class
app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
bootstrap = Bootstrap(app)
mail = Mail(app)
app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/rsmal188/Documents/CUS1166-group-c-dev-small/database.db'
db2 = SQLAlchemy(app)


class User(db2.Model):
    id = db2.Column(db2.Integer, primary_key=True)
    name = db2.Column(db2.String(100), nullable=False)
    username = db2.Column(db2.String(120), unique=True, nullable=False)
    email = db2.Column(db2.String(60), unique=True, nullable=False)
    password = db2.Column(db2.String(60), nullable=False)

#S3 Setup
s3 = FlaskS3()
s3.init_app(app)
app.config['FLASKS3_BUCKET_NAME'] = 'cus1166projectphotos'


# Routes
@app.route("/")
def index():
    return render_template('index.html')


# Search
@app.route("/search", methods=['GET', 'POST'])
def search():
    advanced_search = AdvancedSearchForm()
    page = request.args.get('page', '1')
    page = int(page)
    if request.method == 'POST':
        return search_results(advanced_search, form=advanced_search, page=page)
    return render_template('search.html', form=advanced_search)


@app.route("/search_results/page/<int:page>", methods=['GET', 'POST'])
@app.route("/search_results", defaults={'page': 1}, methods=['GET', 'POST'])
def search_results(advanced_search, form, page):
    results = []
    filter = FilterForm()
    mailform = MailForm()
    if (advanced_search.data['name'] != '' or advanced_search.data['city']
        != '' or advanced_search.data['state'] != ''
        or advanced_search.data['categories'] != ''
            or advanced_search.data['stars'] != ''):
        q1 = advanced_search.data['name']
        q2 = advanced_search.data['city']
        q3 = advanced_search.data['state']
        q4 = advanced_search.data['categories']
        q5 = advanced_search.data['stars']
        # Creating sessions to pass into search_results_filtered
        session['adv_search_name'] = q1
        session['adv_search_city'] = q2
        session['adv_search_state'] = q3
        session['adv_search_categories'] = q4
        session['adv_search_stars'] = q5
        # Get data from query
        results, result_count = db.advanced_search(q1, q2, q3, q4, q5)
        # Pagination
        total = result_count
        page = request.args.get('page', '1')
        page = int(page)
        per_page = 20
        offset = (page - 1) * per_page
        results_for_render = results.skip(offset).limit(per_page)
        pagination = Pagination(
                    page=page,
                    per_page=per_page,
                    offset=offset,
                    total=total,
                    format_total=True,
                    format_number=True,
                    css_framework='bootstrap4')
        if mailform.validate_on_submit():
            # Get data from selected rows in search results table
            selected_list = request.form.getlist('selected_documents')
            # Create and fill lists with data to pass to email template
            (names, addresses, cities, states, postal_codes, stars,
                review_counts, categories) = ([], [], [], [], [], [], [], [])
            lists = zip(names, addresses, cities, states, postal_codes,
                        stars, review_counts, categories)
            for item in selected_list:
                item = json.loads(item)
                names.append(item['name'])
                addresses.append(item['address'])
                cities.append(item['city'])
                states.append(item['state'])
                postal_codes.append(item['postal_code'])
                stars.append(item['stars'])
                review_counts.append(item['review_count'])
                categories.append(item['categories'])
            # Build and send email message
            msg = Message(
                'Mail from CUS1166 Group C',
                recipients=[mailform.recipients.data])
            msg.body = mailform.body.data
            body = msg.body
            msg.html = render_template(
                      'email.html',
                      names=names,
                      addresses=addresses,
                      cities=cities,
                      states=states,
                      postal_codes=postal_codes,
                      stars=stars,
                      review_counts=review_counts,
                      categories=categories,
                      lists=lists,
                      body=body)
            mail.send(msg)
            return redirect('/sent')

    #db.create_photo_id_dictionary(results)
    if not results:
        flash('No results found')
        return redirect('/search')
    else:
        return render_template(
            'search_results.html', form=form, filterform=filter,
            mailform=mailform, results=results, result_count=result_count,
            q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, page=page, per_page=per_page,
            pagination=pagination, results_for_render=results_for_render)


@app.route("/search_results_filtered/page/<int:page>", methods=['GET', 'POST'])
@app.route("/search_results_filtered", defaults={'page': 1},
           methods=['GET', 'POST'])
def search_results_filtered(page):
    results = []
    filter = FilterForm()
    mailform = MailForm()
    if (session['adv_search_name'] != '' or session['adv_search_city'] != ''
        or session['adv_search_state'] != ''
        or session['adv_search_categories'] != ''
            or session['adv_search_stars'] != ''):
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
        pagination = Pagination(
                    page=page,
                    per_page=per_page,
                    offset=offset,
                    total=total,
                    format_total=True,
                    format_number=True,
                    css_framework='bootstrap4')
        if mailform.validate_on_submit():
            selected_list = request.form.getlist('selected_documents')
            (names, addresses, cities, states, postal_codes, stars,
                review_counts, categories) = ([], [], [], [], [], [], [], [])
            lists = zip(names, addresses, cities, states, postal_codes,
                        stars, review_counts, categories)
            for item in selected_list:
                item = json.loads(item)
                names.append(item['name'])
                addresses.append(item['address'])
                cities.append(item['city'])
                states.append(item['state'])
                postal_codes.append(item['postal_code'])
                stars.append(item['stars'])
                review_counts.append(item['review_count'])
                categories.append(item['categories'])
            msg = Message(
                'Mail from CUS1166 Group C',
                recipients=[mailform.recipients.data])
            msg.body = mailform.body.data
            body = msg.body
            msg.html = render_template(
                      'email.html',
                      names=names,
                      addresses=addresses,
                      cities=cities,
                      states=states,
                      postal_codes=postal_codes,
                      stars=stars,
                      review_counts=review_counts,
                      categories=categories,
                      lists=lists,
                      body=body)
            mail.send(msg)
            return redirect('/sent')
        if request.form.get('sortbutton') == "Sort Ascending":
            sortby = filter.data['select']
            sortedresults = db.sort_request(sortby, results, 1)
            return render_template(
                'search_results.html', filterform=filter, mailform=mailform,
                results=sortedresults, result_count=result_count,
                results_for_render=results_for_render, page=page,
                per_page=per_page, pagination=pagination)
        elif request.form.get('sortbutton') == "Sort Descending":
            sortby = filter.data['select']
            sortedresults = db.sort_request(sortby, results, -1)
            return render_template(
                'search_results.html', filterform=filter, mailform=mailform,
                results=sortedresults, result_count=result_count,
                results_for_render=results_for_render, page=page,
                per_page=per_page, pagination=pagination)


# Display
@app.route("/display_info", methods=['GET', 'POST'])
def display_info():
    display = DisplayForm(request.form)

    if (session['display_info_name'] != '' or session['display_info_hours']
        != '' or session['display_info_latitude'] != ''
            or session['display_info_longitude'] != ''):
        d1 = session['display_info_name']
        d2 = session['display_info_hours']
        d3 = session['display_info_latitude']
        d4 = session['display_info_longitude']

    if request.form.get('displaybutton') == "Display Info":
        displayby = display.data['select']
        displayedresults = db.display_info(displayby, results, 1)
        return render_template(
            'display_info.html', displayform=display, results=displayedresults,
            result_count=result_count)


@app.route("/new_restaurant", methods=['GET', 'POST'])
def new_restaurant():
    form = RestaurantForm()
    if request.method == 'POST' and form.validate():
        # save the restaurant
        restaurant = Restaurant()
        save_changes(restaurant, form, new=True)
        flash('Restaurant created successfully!')
        return redirect('/')
    return render_template('new_restaurant.html', form=form)

    def submit(restaurant, form, new=False):
        restaurant = Restaurant()
        restaurant.name = form.restaurant.data
        restaurant.name = name
        restaurant.city = form.city.data
        restaurant.state = form.state.data
        restaurant.is_open = form.is_open.data

    if new:
        db_session.add(restaurant)
        db_session.commit()


# Edit
@app.route("/item/<int:id>", methods=['GET', 'POST'])
def edit(id):

    qry = db.query(Restaurant).filter(Restaurant).id == id
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
    registered_user = User.query.filter_by(
                     username=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    user = User(
          request.form['name'],
          request.form['username'],
          request.form['email'],
          request.form['password'],
          request.form['confirm'])

    db.session.add(new_user)
    db.session.commit()

    flash('New User Created!')
    return redirect('/login')

    return render_template('register.html', form=form)


@app.route("/sent")
def sent():
    return render_template('sent.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5110))
    app.run(debug=True, host='0.0.0.0', port=port)
