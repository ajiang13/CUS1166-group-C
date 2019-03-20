#Imports
from flask import Flask, render_template, url_for, request, redirect, flash, session
import json
import db
from tables import Results
from forms import SearchForm, FilterForm, WelcomeForm


# Create an instance of Flask class
app = Flask(__name__, template_folder='templates')
app.secret_key = "key"

#Routes
@app.route("/")
def index():
    welcome = WelcomeForm(request.form)
    return render_template('index.html', welcomeform = welcome)

#Search
@app.route("/search", methods=['GET', 'POST'])
def search():
    search = SearchForm(request.form)
    session['search'] = search.data['search']
    search_string = session['search']
    if request.method == 'POST':
        return search_results()
    return render_template('search.html', form=search)

@app.route("/search_results", methods=['GET', 'POST'])
def search_results():
    results = []
    search_string = session['search']
    filter = FilterForm(request.form)

    if search_string != '' and not request.action['search_results_filtered']:
        results = db.search_business_name(search_string)
        result_count = db.search_business_count(search_string)
    if not results:
        flash('No results found')
        return redirect('/search')
    else:
        return render_template('search_results.html', search=search, results=results, result_count=result_count, search_string=search_string, form2 = filter)

@app.route("/search_results_filtered", methods=['GET', 'POST'])
def search_results_filtered():
    search_string = session['search']
    results = db.search_business_name(search_string)
    filter = FilterForm(request.form)
    sortby = filter.data['select']
    ordering = 'Ascending'
    #ordering = filter.data['selectorder']

    #Determining if data is to be sorted and sorting if so
    if ordering == 'Ascending':
        results = db.sort_request(sortby, results, False)
        result_count = db.search_business_count(search_string)
        return search_results()
    else:
        results = db.sort_request(sortby, results, True)
        result_count = db.search_business_count(search_string)
        return search_results()


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)
