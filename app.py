# Imports
from werkzeug.utils import secure_filename

from config import Config
from flask import (Flask, render_template, url_for, request, redirect, flash,
                   session, jsonify)
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_paginate import Pagination, get_page_args
from forms import (AdvancedSearchForm, FilterForm, RestaurantForm, MailForm,
                   DisplayForm, RegistrationForm)
import db

# Create an instance of Flask class
app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
bootstrap = Bootstrap(app)
mail = Mail(app)
app.secret_key = "key"


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
            #checked_results = request.form.to_dict(flat=False)
            #checked_results = {}
            #for key in checked_data.keys():
            #    for value in checked_data.getlist(key):
            #        checked_results.update(checked_data)
            checked_results = request.form.getlist('selected_documents')
            #checked_results = []
            #for document in results_list:
            #    checked_results.append({document})
            msg = Message(
                'Mail from CUS1166 Group C',
                recipients=[mailform.recipients.data])
            msg.body = mailform.body.data
            body = msg.body
            msg.html = render_template(
                      'email.html',
                      checked_results=checked_results,
                      body=body)
            mail.send(msg)
            #print(results)
            #for keys in results:
            #    print(keys.values)
            print(checked_results)
            #for document in checked_results:
            #    print(document.name)
            return redirect('/sent')
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
            msg = Message(
                'Mail from CUS1166 Group C',
                recipients=[form.recipients.data])
            msg.body = form.body.data
            mail.send(msg)
            return redirect('/sent')
    if not results:
        flash('No results found')
        return redirect('/search')
    if request.form.get('sortbutton') == 'Sort Ascending':
        sortby = filter.data['select']
        sortedresults = db.sort_request(sortby, results, 1)
        return render_template(
            'search_results.html', filterform=filter, mailform=mailform,
            results=sortedresults, result_count=result_count,
            results_for_render=results_for_render, page=page,
            per_page=per_page, pagination=pagination)
    elif request.form.get('sortbutton') == 'Sort Descending':
        sortby = filter.data['select']
        sortedresults = db.sort_request(sortby, results, -1)
        #sortedresults = db.filter_by_stars(results, 3)
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

#Add
@app.route("/new_restaurant", methods=['GET', 'POST'])
def new_restaurant():
    add_restaurant = RestaurantForm()
    if (add_restaurant.data['name'] != '' or add_restaurant.data['address']
        != '' or add_restaurant.data['city'] != ''
            or add_restaurant.data['state'] != ''
                or add_restaurant.data['zip_code'] != ''
                    or add_restaurant.data['categories'] != ''):
        a1 = add_restaurant.data['name']
        a2 = add_restaurant.data['address']
        a3 = add_restaurant.data['city']
        a4 = add_restaurant.data['state']
        a5 = add_restaurant.data['zip_code']
        a6 = add_restaurant.data['categories']
        db.add_restaurant(a1, a2, a3, a4, a5, a6)
        return render_template('new_restaurant.html', form=add_restaurant,
                a1=a1, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6)
    flash("Restaurant successfully added!")
    return redirect('/new_restaurant')

# Edit
@app.route("/edit", methods=['GET', 'POST'])
def edit():
    edit_restaurant = RestaurantForm()
    if (edit_restaurant.data['name'] != '' or edit_restaurant.data['address']
        != '' or edit_restaurant.data['city'] != ''
            or edit_restaurant.data['state'] != ''
                or edit_restaurant.data['zip_code'] != ''
                    or edit_restaurant.data['categories'] != ''):
        e1 = edit_restaurant.data['name']
        e2 = edit_restaurant.data['address']
        e3 = edit_restaurant.data['city']
        e4 = edit_restaurant.data['state']
        e5 = edit_restaurant.data['zip_code']
        e6 = edit_restaurant.data['categories']
        db.edit_restaurant(e1, e2, e3, e4, e5, e6)
        return render_template('edit.html', form=edit_restaurant,
                e1=e1, e2=e2, e3=e3, e4=e4, e5=e5, e6=e6, query=query)
    flash("The restaurant has been updated!")
    return redirect('/edit')



# login
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin' or request.form['password']
                != 'admin'):
                error = 'Invalid Credentials. Please Try Again.'
        else:
            return redirect('/')
    return render_template('login.html', error=error)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        return render_template('index.html')
    return render_template('register.html', form=form)


@app.route("/sent")
def sent():
    return render_template('sent.html')


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)
