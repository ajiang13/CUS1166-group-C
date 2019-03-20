from flask import Flask render_template, url_for, request, redirect, flash
import json
from backend import db
app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5110)
