#Imports
from flask import Flask, render_template, url_for, request, redirect, flash, session
import json
import db
from tables import Results
from forms import SearchForm, AdvancedSearchForm, FilterForm

# Create an instance of Flask class
app = Flask(__name__, template_folder='templates')
app.secret_key = "key"

#Routes
@app.route("/")
def index():
    return render_template('index.html')

#Search
@app.route("/search", methods=['GET', 'POST'])
def search():
    search = SearchForm(request.form)
    advanced_search = AdvancedSearchForm(request.form)
    #TO-DO - fix issue: submitting advanced search form raises an error due to first form being empty
    if request.method == 'POST':
        if request.form['button'] == 'Search':
            advanced_search = request.form.get('Advanced Search')
            session['advanced_search'] = advanced_search
            return search_results(search, advanced_search, form=search)
        elif request.form['button'] == 'Advanced Search':
            search = request.form.get('select')
            session['search'] = search
            return search_results(search, advanced_search, form=advanced_search)
    return render_template('search.html', form=search, form2=advanced_search)

@app.route("/search_results", methods=['GET', 'POST'])
def search_results(search, advanced_search, form):
    results = []
    search_string = []
    filter = FilterForm(request.form)

    #Creating sessions to pass into search_results_filtered
    session['selection'] = search.data['select']
    session['search_string'] = search.data['search']

    if search.data['select'] == 'Name' and search.data['search'] != '':
        search_string = search.data['search']
        results = db.search_business_name(search_string)
        result_count = db.search_business_count(search_string)
    elif search.data['select'] == 'City' and search.data['search'] != '':
        search_string = search.data['search']
        results = db.search_city(search_string)
        result_count = db.search_city_count(search_string)
    elif search.data['select'] == 'State' and search.data['search'] != '':
        search_string = search.data['search']
        results = db.search_state(search_string)
        result_count = db.search_state_count(search_string)
    elif search.data['select'] == 'Categories' and search.data['search'] != '':
        search_string = search.data['search']
        results = db.search_categories(search_string)
        result_count = db.search_categories_count(search_string)
    elif search.data['select'] != '':
        search_string = search.data['stars']
        results = db.search_stars(search_string)
        result_count = db.search_stars_count(search_string)
    elif advanced_search.data['name'] != '' or advanced_search.data['city'] != '' or advanced_search.data['state'] != '' or advanced_search.data['categories'] != '' or advanced_search.data['stars'] != '':
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

        search_string = {}
        if q1 != 'null':
            search_string.append({'$text': {'$search': q1}},)
        if q2 != 'null':
            search_string.append({'city': {'$regex': q2, '$options': 'i'}},)
        if q3 != 'null':
            search_string.append({'state': {'$regex': q3, '$options': 'i'}},)
        if q4 != 'null':
            search_string.append({'categories': {'$regex': q4, '$options': 'i'}},)
        if q5 != 'null':
            search_string.append({'stars': {'$gte': q5}},)
        results = db.advanced_search(search_string)
        result_count = db.advanced_search_count(search_string)
    if not results:
        flash('No results found')
        return redirect('/search')
    else:
        table = Results(results)
        table.border = True
        return render_template('search_results.html', search=search, form=form, filterform = filter, results=results, result_count=result_count, search_string=search_string, table =table)



@app.route("/search_results_filtered", methods=['GET', 'POST'])
def search_results_filtered():
    results = []
    search_string = []
    filter = FilterForm(request.form)
    min_stars = filter.data['stars']

    #Determing which field to search by(Default search), results = search_field
    if session['selection'] == 'Name' and session['search_string'] != '':
        search_string = session['search_string']
        results = db.search_business_name(search_string)
        result_count = db.search_business_count(search_string)
    elif session['selection'] == 'City' and session['search_string'] != '':
        search_string = session['search_string']
        results = db.search_city(search_string)
        result_count = db.search_city_count(search_string)
    elif session['selection'] == 'State' and session['search_string'] != '':
        search_string = session['search_string']
        results = db.search_state(search_string)
        result_count = db.search_state_count(search_string)
    elif session['selection'] == 'Categories' and session['search_string'] != '':
        search_string = session['search_string']
        results = db.search_categories(search_string)
        result_count = db.search_categories_count(search_string)
    elif session['selection'] != '':
        search_string = session['search_string']
        results = db.search_stars(search_string)
        result_count = db.search_stars_count(search_string)
    #If any info is entered into the advanced search fields, results = advanced_search
    elif session['adv_search_name'] != '' or session['adv_search_city'] != '' or session['adv_search_state'] != '' or session['adv_search_categories'] != '' or session['adv_search_stars'] != '':
        q1 = advanced_search.data['name']
        q2 = advanced_search.data['city']
        q3 = advanced_search.data['state']
        q4 = advanced_search.data['categories']
        q5 = advanced_search.data['stars']
        search_string = {}
        if q1 != 'null':
            search_string.append({'$text': {'$search': q1}},)
        if q2 != 'null':
            search_string.append({'city': {'$regex': q2, '$options': 'i'}},)
        if q3 != 'null':
            search_string.append({'state': {'$regex': q3, '$options': 'i'}},)
        if q4 != 'null':
            search_string.append({'categories': {'$regex': q4, '$options': 'i'}},)
        if q5 != 'null':
            search_string.append({'stars': {'$gte': q5}},)
        results = db.advanced_search(search_string)
        result_count = db.advanced_search_count(search_string)

    if not results:
        flash('No results found')
        return redirect('/search_results')
    if request.form['sortbutton'] == "Sort Ascending" and not min_stars:
        sortby = filter.data['select']
        sortedresults = db.sort_request(sortby,results,1)
        return render_template('search_results.html', search=search, filterform = filter, results=sortedresults, result_count=result_count, search_string=search_string)
    else:
        sortby = filter.data['select']
        sortedresults = db.sort_request(sortby,results,-1)
        #sortedresults = db.filter_by_stars(results, 3)
        return render_template('search_results.html', search=search, filterform = filter, results=sortedresults, result_count=result_count, search_string=search_string)

#Edit
@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Restaurant).filter(Restaurant).id==id)
    restaurant = qry.first()

    if restaurant:
        form = AlbumForm(formdata=request.form, obj=restaurant)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(restaurant, form)
            flash('Restaurant updated successfully!')
            return redirect('/')
        return render_template('edit_restaurant.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


#login
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please Try Again.'
        else:
            return redirect('/')
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)
