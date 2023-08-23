'''The code sets up a Flask web application that connects to a SQLite database 
    to fetch data about sports matches, odds, and bookmakers. The code also includes a dictionary
    of bookie URLs'''

from flask import Flask, render_template
import sqlite3
from LoginCheck.RapidApiSport import *
from main import *
# I could have done whats below in the database but wanted to show variety and use of dictionary
# It allows the Bookies to be linked to their site so if user wants to place the bet, he has quick
#  access to the bookmakers site

bookie_urls = {
    "Unibet": "https://www.unibet.com",
    "DraftKings": "https://www.draftkings.com",
    "Bovada": "https://www.bovada.lv",
    "FanDuel": "https://www.fanduel.com",
    "PointsBet (US)": "https://www.pointsbet.com",
    "William Hill (US)": "https://www.williamhill.com",
    "MyBookie.ag": "https://www.mybookie.ag",
    "Barstool Sportsbook": "https://www.barstoolsportsbook.com",
    "BetMGM": "https://www.betmgm.com",
    "SuperBook": "https://www.superbook.com",
    "BetOnline.ag": "https://www.betonline.ag",
    "BetUS": "https://www.betus.com",
    "BetRivers": "https://www.betrivers.com",
    "LowVig.ag": "https://www.lowvig.ag",
    "WynnBET": "https://www.wynnbet.com",
    "TwinSpires": "https://www.twinspires.com",
    "Virgin Bet": "https://www.virginbet.com",
    "Ladbrokes": "https://www.ladbrokes.com",
    "888sport": "https://www.888sport.com",
    "Bet Victor": "https://www.betvictor.com",
    "Betfair Sportsbook": "https://www.betfair.com/sport",
    "Paddy Power": "https://www.paddypower.com",
    "LiveScore Bet": "https://www.livescorebet.com",
    "Coral": "https://www.coral.co.uk",
    "Betway": "https://www.betway.com",
    "Casumo": "https://www.casumo.com",
    "LeoVegas": "https://www.leovegas.com",
    "Mr Green": "https://www.mrgreen.com",
    "Betfair": "https://www.betfair.com",
    "Matchbook": "https://www.matchbook.com",
    "William Hill": "https://www.williamhill.com",
    "Sky Bet": "https://www.skybet.com",
    "BoyleSports": "https://www.boylesports.com"
}

app = Flask(__name__) #a Flask app instance
app.secret_key = "i_bet_you_cannot_guess_it" #for session security 

# Function to retrieve leagues, matches, and odds data from database
def get_leagues_and_matches_from_db():
    conn = sqlite3.connect('sports_oddyy.db')
    cursor = conn.cursor()

    # SQL query to retrieve match information along with odds and bookmaker details
    cursor.execute("""
        SELECT m.Description, m.HomeTeam, m.AwayTeam, p.HomePrice, p.AwayPrice, p.DrawPrice, b.NAME
        FROM PRICE p
        JOIN Matches m ON p.MatchID = m.ID
        JOIN BOOKMAKERS b ON p.BookieID = b.ID
    """)
    
    data = cursor.fetchall() # Fetch all the rows of data returned by the query

    conn.close()

    return data


@app.route("/")
def index():
    
    data = get_leagues_and_matches_from_db() # Call the function to retrieve data from the database

    
    league_matches = {} # Create a dictionary to store matches grouped by leagues

    # Loop through each row of data fetched from the database
    for row in data:
        league = row[0]
        match_data = {
            "home_team": row[1],
            "away_team": row[2],
            "home_price": row[3],
            "away_price": row[4],
            "draw_price": row[5],
            "bookie": row[6]
        }

        # Check if the league is already in the dictionary and if it is, append the match data to the existing list of matches for that league
        if league in league_matches:
            league_matches[league].append(match_data)
        else:
            
            league_matches[league] = [match_data] # If the league is not in dictionary, create a new list for the league and add the match data to it

    # Render an HTML template, passing the league_matches dictionary and bookie_urls to the template
    return render_template("index.html", league_matches=league_matches, bookie_urls=bookie_urls)


if __name__ == '__main__':
    setup_initial_data(sportsdbfile)  # Call the function from main to make sure data displayed is most recent
    app.run(debug=True)