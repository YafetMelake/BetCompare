import re

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


def check_email(email):
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    return True if re.search(regex, email) else False
