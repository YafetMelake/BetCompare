import requests
import sqlite3

API_KEY = '07556a48f189162eef6239585994f7f2'

SPORT = 'soccer'  # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'uk, eu'  # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h'  # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal'  # decimal | american

DATE_FORMAT = 'iso'  # iso | unix

def sports_odds():

    odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)
    return odds_response.json()


def save_sports(key, sportsdbfile):
    conn = sqlite3.connect(sportsdbfile)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS ODDSTABLE (SPORT TEXT, BOOKIE TEXT, HOMETEAM TEXT, HOMEPRICE REAL, AWAYTEAM TEXT, AWAYPRICE REAL)")

    home_price = None
    away_price = None

    bookmaker_key = key["bookmakers"][0]["key"]

    markets = key["bookmakers"][0]["markets"]
    for market in markets:
        if market["key"] == "h2h":
            outcomes = market["outcomes"]
            for outcome in outcomes:
                if outcome["name"] == key["home_team"]:
                    home_price = outcome["price"]
                elif outcome["name"] == key["away_team"]:
                    away_price = outcome["price"]

    cursor.execute("""
        INSERT INTO ODDSTABLE(SPORT, BOOKIE, HOMETEAM, HOMEPRICE, AWAYTEAM, AWAYPRICE)
        VALUES(?, ?, ?, ?, ?, ?)""",
        (key["sport_key"], bookmaker_key, key["home_team"], home_price, key["away_team"], away_price)
    )

    conn.commit()
    conn.close()

def bookmakers_table(sportsdbfile, response_data):
    conn = sqlite3.connect(sportsdbfile)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS BOOKMAKERS (ID INTEGER PRIMARY KEY, NAME TEXT)")

    for key in response_data:
        bookmakers = key["bookmakers"]
        for bookmaker in bookmakers:
            cursor.execute("INSERT OR IGNORE INTO BOOKMAKERS (NAME) VALUES (?)", (bookmaker["title"],))

    conn.commit()
    conn.close()

def matches_table(sportsdbfile, response_data):
    conn = sqlite3.connect(sportsdbfile)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Matches (ID INTEGER PRIMARY KEY, Date TEXT, Description TEXT, HomeTeam TEXT, AwayTeam TEXT)")

    for key in response_data:
        date = key.get("commence_time")
        description = key.get("sport_key")
        home_team = key.get("home_team")
        away_team = key.get("away_team")

        cursor.execute("INSERT OR IGNORE INTO Matches (Date, Description, HomeTeam, AwayTeam) VALUES (?, ?, ?, ?)",
                       (date, description, home_team, away_team))

    conn.commit()
    conn.close()

def price_table(sportsdbfile, response_data):
    conn = sqlite3.connect(sportsdbfile)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS PRICE (BookieID INTEGER, MatchID INTEGER, HomePrice REAL, AwayPrice REAL, DrawPrice REAL)")

    for key in response_data:
        bookmakers = key["bookmakers"]
        for bookmaker in bookmakers:
            cursor.execute("INSERT OR IGNORE INTO BOOKMAKERS (NAME) VALUES (?)", (bookmaker["title"],))

        markets = key["bookmakers"][0]["markets"]
        for market in markets:
            if market["key"] == "h2h":
                outcomes = market["outcomes"]
                home_price = None
                away_price = None
                draw_price = None  # Initialize draw_price variable

                for outcome in outcomes:
                    if outcome["name"] == key["home_team"]:
                        home_price = outcome["price"]
                    elif outcome["name"] == key["away_team"]:
                        away_price = outcome["price"]
                    elif outcome["name"] == "Draw":
                        draw_price = outcome["price"]  # Assign draw price

                cursor.execute("SELECT ID FROM BOOKMAKERS WHERE NAME=?", (key["bookmakers"][0]["title"],))
                bookie_id = cursor.fetchone()
                if bookie_id is not None:
                    bookie_id = bookie_id[0]

                cursor.execute("SELECT ID FROM Matches WHERE HomeTeam=? AND AwayTeam=?", (key["home_team"], key["away_team"]))
                match_id = cursor.fetchone()
                if match_id is not None:
                    match_id = match_id[0] 

                cursor.execute("INSERT INTO PRICE (BookieID, MatchID, HomePrice, AwayPrice, DrawPrice) VALUES (?, ?, ?, ?, ?)",
                               (bookie_id, match_id, home_price, away_price, draw_price))

    conn.commit()
    conn.close()



def sportssoddss(sportsdbfile):
    response_data = sports_odds()
    bookmakers_table(sportsdbfile, response_data)
    matches_table(sportsdbfile, response_data)
    price_table(sportsdbfile, response_data)

    for key in response_data:
        save_sports(key, sportsdbfile)
        print(key)