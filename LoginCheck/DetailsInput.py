'''authentication function prompts user to enter email and uses the check_email and make_account
    function to validate and verify the details entered and if so, adds the details to the database'''

from LoginCheck.RegExEmailCheck import *
from LoginCheck.StoringEmails import *

def authentication(sportsdbfile):
    while True:
        email = input("Please enter your Email: ")
        valid_email = check_email(email)
        while not valid_email:
            email = input("Please enter another Email as this is not Valid: ")
            valid_email = check_email(email)

        print(
            "Please now enter a password, make it as secure or as weak as you want..."
        )
        valid_password = input("Password:")

        if make_account(email, valid_password, sportsdbfile):
            break

