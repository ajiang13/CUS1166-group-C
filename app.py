#Imports
from flask import Flask, render_template, url_for, request, redirect, jsonify
import json
from backend import db

# Create an instance of Flask class
app = Flask(__name__, template_folder='templates')

#Routes
@app.route("/")
def index():
    return render_template('index.html')

#Search
@app.route("/search", methods = ['GET', 'POST'])
def search():
    query = request.form.get('name')
    if request.method == 'POST':
        db.search_business_name('query')
        return redirect(url_for('search_results', query=query, results=results, result_count=result_count))
    return render_template('search.html')

@app.route("/search_results", methods = ['GET', 'POST'])
def search_results():
    return render_template('search_results.html')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)
