from flask import render_template
from app import app_lol


@app_lol.route('/')
@app_lol.route('/index')
def index():
    matches = ['None']
    return render_template('matches.html', title='Matches', matches=matches)
    