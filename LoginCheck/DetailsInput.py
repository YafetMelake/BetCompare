from RapidApiEmailCheck import check_email
from StoringEmails import make_account

def authentication():
    while True: 
        email = input("Please enter your Email: ")
        valid_email = check_email(email)
        while not valid_email:
            email = input("Please enter another Email as this is not Valid: ")
            valid_email = check_email(email)

        print("Please now enter a password, make it as secure or as weak as you want...")
        valid_password = input("Password:")

        if make_account(email, valid_password):
            break
    
authentication()