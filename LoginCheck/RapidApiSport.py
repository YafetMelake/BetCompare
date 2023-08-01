import requests
import sqlite3

def sports_odds():
    url = "https://odds.p.rapidapi.com/v4/sports/upcoming/odds"

    querystring = {"regions":"us","oddsFormat":"decimal","markets":"h2h,spreads","dateFormat":"iso"}

    headers = {
        "X-RapidAPI-Key": "c7d2f04cc3msh688208d8fd9079dp1d3c72jsnfa46ed8c8d2f",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    odds_response = requests.get(url, headers=headers, params=querystring)
    return odds_response.json()


def save_sports(key, sportsdbfile):
    conn = sqlite3.connect(sportsdbfile)
    cursor = conn.cursor()

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

    cursor.execute("CREATE TABLE IF NOT EXISTS PRICE (ID INTEGER PRIMARY KEY, BookieID INTEGER, MatchID INTEGER, HomePrice REAL, AwayPrice REAL, FOREIGN KEY(BookieID) REFERENCES BOOKMAKERS(ID), FOREIGN KEY(MatchID) REFERENCES Matches(ID))")

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
                for outcome in outcomes:
                    if outcome["name"] == key["home_team"]:
                        home_price = outcome["price"]
                    elif outcome["name"] == key["away_team"]:
                        away_price = outcome["price"]

                cursor.execute("SELECT ID FROM BOOKMAKERS WHERE NAME=?", (key["bookmakers"][0]["title"],))
                bookie_id = cursor.fetchone()
                if bookie_id is not None:
                    bookie_id = bookie_id[0]

                cursor.execute("SELECT ID FROM Matches WHERE HomeTeam=? AND AwayTeam=?", (key["home_team"], key["away_team"]))
                match_id = cursor.fetchone()
                if match_id is not None:
                    match_id = match_id[0] 

                cursor.execute("INSERT INTO PRICE (BookieID, MatchID, HomePrice, AwayPrice) VALUES (?, ?, ?, ?)",
                               (bookie_id, match_id, home_price, away_price))

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