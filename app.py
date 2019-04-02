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
    advanced_search = AdvancedSearchForm(request.form)
    #TO-DO - fix issue: submitting advanced search form raises an error due to first form being empty
    if request.method == 'POST':
        if request.form['button'] == 'Advanced Search':
            return search_results(advanced_search, form=advanced_search)
    return render_template('search.html', form=advanced_search)

@app.route("/search_results", methods=['GET', 'POST'])
def search_results(advanced_search, form):
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
    if not results:
        flash('No results found')
        return redirect('/search')
    else:
        return render_template('search_results.html', form=form, filterform = filter, results=results, result_count=result_count, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5)

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
    if not results:
        flash('No results found')
        return redirect('/search')
    if request.form['sortbutton'] == "Sort Ascending":
        sortby = filter.data['select']
        sortedresults = db.sort_request(sortby,results,1)
        return render_template('search_results.html', filterform = filter, results=sortedresults, result_count=result_count)
    else:
        sortby = filter.data['select']
        sortedresults = db.sort_request(sortby,results,-1)
        #sortedresults = db.filter_by_stars(results, 3)
        return render_template('search_results.html', filterform = filter, results=sortedresults, result_count=result_count)


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
