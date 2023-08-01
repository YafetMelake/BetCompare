from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = "i_bet_you_cannot_guess_it"

def get_prices_from_db():
    conn = sqlite3.connect('sports_oddyy.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.BookieID, m.HomeTeam, m.AwayTeam, p.HomePrice, p.AwayPrice
        FROM PRICE p
        JOIN Matches m ON p.MatchID = m.ID
    """)
    data = cursor.fetchall()

    conn.close()
    return data

@app.route("/")
def index():
    data = get_prices_from_db()
    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
