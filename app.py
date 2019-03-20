#Imports
from flask import Flask, render_template, url_for, request, redirect, flash
import json
import db
from tables import Results
from forms import SearchForm

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
    if request.method == 'POST':
        return search_results(search)
    return render_template('search.html', form=search)

@app.route("/search_results", methods=['GET', 'POST'])
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] != '':
        results = db.search_business_name(search_string)
        result_count = db.search_business_count(search_string)
    if not results:
        flash('No results found')
        return redirect('/search')
    else:
        return render_template('search_results.html', search=search, results=results, result_count=result_count, search_string=search_string)

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
