import requests
import sqlite3

# def sports():
#     url = "https://odds.p.rapidapi.com/v4/sports"
#     querystring = {"all": "true"}
#     headers = {
#         "X-RapidAPI-Key": "c7d2f04cc3msh688208d8fd9079dp1d3c72jsnfa46ed8c8d2f",
#         "X-RapidAPI-Host": "odds.p.rapidapi.com"
#     }
#     response = requests.get(url, headers=headers, params=querystring)
#     return response.json()


# def save_sports(key):
#     conn = sqlite3.connect("sports.db")
#     cursor = conn.cursor()
    
#     cursor.execute(""" INSERT INTO SPORTSSS(KEY, GROUPYafet, DESCRIPTION, OUTRIGHTS, TITLE) VALUES(?,?,?,?,?)""", (key["key"], key["group"], key["description"], key["has_outrights"], key["title"]))
	
#     conn.commit()
#     conn.close()




def sports_odds():
    url = "https://odds.p.rapidapi.com/v4/sports/upcoming/odds"

    querystring = {"regions":"us","oddsFormat":"decimal","markets":"h2h,spreads","dateFormat":"iso"}

    headers = {
        "X-RapidAPI-Key": "c7d2f04cc3msh688208d8fd9079dp1d3c72jsnfa46ed8c8d2f",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    odds_response = requests.get(url, headers=headers, params=querystring)
    return odds_response.json()


def save_sports(key):
    conn = sqlite3.connect("sports_oddy.db")
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

response_data = sports_odds()

for key in response_data:
    save_sports(key)
    print(key)

sports_odds()