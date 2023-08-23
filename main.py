# main.py
sportsdbfile = "C:/Users/yafet/Documents/GitHub/BetCompare/sports_oddyy.db"
from LoginCheck.DetailsInput import authentication
from LoginCheck.RapidApiSport import sportssoddss
import os
import sqlite3

# Function to set up initial data for the sports odds application.
# This function is designed to be called from app.py to ensure that app.py displays the most recent data.
# Scheduling app.py to run this function can keep the data up-to-date without deploying the entire application.
def setup_initial_data(sportsdbfile):
    # Delete or truncate the existing data in the database to allow for the new data to be 
    # displayed when app.py is scheduled to update on pythonanywhere
    if os.path.exists(sportsdbfile):
        connection = sqlite3.connect(sportsdbfile)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM PRICE") 
        connection.commit()
        connection.close()

    # authentication(sportsdbfile)
    sportssoddss(sportsdbfile)
