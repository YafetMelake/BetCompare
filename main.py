# main.py
sportsdbfile = "C:/Users/yafet/Documents/GitHub/BetCompare/sports_oddyy.db"
from LoginCheck.DetailsInput import authentication
from LoginCheck.RapidApiSport import sportssoddss

# Function to set up initial data for the sports odds application.
# This function is designed to be called from app.py to ensure that app.py displays the most recent data.
# Scheduling app.py to run this function can keep the data up-to-date without deploying the entire application.
def setup_initial_data():

    # authentication(sportsdbfile)
    sportssoddss(sportsdbfile)
