import sqlite3
import requests
from flask import Flask, session, render_template, request, g
import os

app = Flask(__name__)
app.secret_key = "i_bet_you_cannot_guess_it"

@app.route("/")
def index():
    data = get_db()
    return render_template("index.html")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g.__database = sqlite3.connect('sports_oddy.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM PRICES")
    return cursor.fetchall()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()
