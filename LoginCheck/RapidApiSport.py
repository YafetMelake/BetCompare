import requests
import sqlite3

API_KEY = '07556a48f189162eef6239585994f7f2'

SPORT = 'Soccer'
REGIONS = 'uk'
MARKETS = 'h2h'
ODDS_FORMAT = 'decimal'
DATE_FORMAT = 'iso'

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

    cursor.execute("CREATE TABLE IF NOT EXISTS ODDSTABLE (SPORT TEXT, BOOKIE TEXT, HOMETEAM TEXT, HOMEPRICE REAL, AWAYTEAM TEXT, AWAYPRICE REAL, UNIQUE(BOOKIE, HOMETEAM, AWAYTEAM))")

    home_price = None
    away_price = None
    bookmaker_key = None

    if "bookmakers" in key and key["bookmakers"]:
        bookmakers = key["bookmakers"]
        if "markets" in bookmakers[0] and bookmakers[0]["markets"]:
            markets = bookmakers[0]["markets"]
            for market in markets:
                if market["key"] == "h2h":
                    outcomes = market["outcomes"]
                    for outcome in outcomes:
                        if outcome.get("name") == key.get("home_team"):
                            home_price = outcome.get("price")
                        elif outcome.get("name") == key.get("away_team"):
                            away_price = outcome.get("price")
                    bookmaker_key = bookmakers[0].get("key")

    cursor.execute("""
        INSERT OR IGNORE INTO ODDSTABLE(SPORT, BOOKIE, HOMETEAM, HOMEPRICE, AWAYTEAM, AWAYPRICE)
        VALUES(?, ?, ?, ?, ?, ?)""",
        (key.get("sport_key"), bookmaker_key, key.get("home_team"), home_price, key.get("away_team"), away_price)
    )

    conn.commit()
    conn.close()

def bookmakers_table(sportsdbfile, response_data):
    conn = sqlite3.connect(sportsdbfile)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS BOOKMAKERS (ID INTEGER PRIMARY KEY, NAME TEXT UNIQUE)")

    for key in response_data:
        bookmakers = key["bookmakers"]
        for bookmaker in bookmakers:
            cursor.execute("INSERT OR IGNORE INTO BOOKMAKERS (NAME) VALUES (?)", (bookmaker["title"],))

    conn.commit()
    conn.close()

def matches_table(sportsdbfile, response_data):
    conn = sqlite3.connect(sportsdbfile)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Matches (ID INTEGER PRIMARY KEY, Date TEXT, Description TEXT, HomeTeam TEXT, AwayTeam TEXT, UNIQUE(Date, HomeTeam, AwayTeam))")

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

    cursor.execute("CREATE TABLE IF NOT EXISTS PRICE (BookieID INTEGER, MatchID INTEGER, HomePrice REAL, AwayPrice REAL, DrawPrice REAL, UNIQUE(BookieID, MatchID))")

    for key in response_data:
        if "bookmakers" in key and key["bookmakers"]:
            bookmakers = key["bookmakers"]
            for bookmaker in bookmakers:
                cursor.execute("INSERT OR IGNORE INTO BOOKMAKERS (NAME) VALUES (?)", (bookmaker.get("title", ""),))

            if "markets" in bookmakers[0] and bookmakers[0]["markets"]:
                markets = bookmakers[0]["markets"]
                for market in markets:
                    if market["key"] == "h2h":
                        outcomes = market.get("outcomes", [])
                        home_price = None
                        away_price = None
                        draw_price = None  

                        for outcome in outcomes:
                            if outcome.get("name") == key.get("home_team"):
                                home_price = outcome.get("price")
                            elif outcome.get("name") == key.get("away_team"):
                                away_price = outcome.get("price")
                            elif outcome.get("name") == "Draw":
                                draw_price = outcome.get("price")  

                        cursor.execute("SELECT ID FROM BOOKMAKERS WHERE NAME=?", (bookmaker.get("title", ""),))
                        bookie_id = cursor.fetchone()
                        if bookie_id is not None:
                            bookie_id = bookie_id[0]

                        cursor.execute("SELECT ID FROM Matches WHERE HomeTeam=? AND AwayTeam=?", (key.get("home_team"), key.get("away_team")))
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
