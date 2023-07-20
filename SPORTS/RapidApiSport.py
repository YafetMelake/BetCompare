import requests
import sqlite3

def sports():
    url = "https://odds.p.rapidapi.com/v4/sports"
    querystring = {"all": "true"}
    headers = {
        "X-RapidAPI-Key": "c7d2f04cc3msh688208d8fd9079dp1d3c72jsnfa46ed8c8d2f",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def save_sports(key):
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    
    cursor.execute(''' INSERT INTO SPORTSSS(KEY, GROUPYafet, DESCRIPTION, OUTRIGHTS, TITLE) VALUES(?,?,?,?,?)''', (key['key'], key['group'], key['description'], key['has_outrights'], key['title']))
	
    conn.commit()
    conn.close()

response_data = sports()

for key in response_data:
    save_sports(key)
    print(key)
