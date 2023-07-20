from RapidApiEmailCheck import get_email
from StoringEmails import make_account

def authentication():
    while True: 
        email = input("Please enter your Email: ")
        valid_email = get_email(email)
        while not valid_email:
            email = input("Please enter another Email as this is not Valid: ")
            valid_email = get_email(email)

        print("Please now enter a password")
        valid_password = input("Password:")

        if make_account(valid_email, valid_password):
            break
    