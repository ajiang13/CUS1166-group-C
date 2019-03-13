#Imports
from flask import Flask, render_template, url_for, request, redirect, flash
import json
from backend import db
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
    if search.data['search'] == '':
        qry = db.search_business_name('search_string')
        results = qry.all()
    if not results:
        flash('No results found')
        return redirect('/search')
    else:
        return render_template('search_results.html', results=results)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)
