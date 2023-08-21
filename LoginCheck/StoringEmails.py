'''currently commented out but this make_account function informs the user to enter an email 
    and password and adds it to the ACCOUNTS table in the database but also checks to see
    if the account already exists. If so it informs the user that the account with the email
    already exists'''

import sqlite3

def make_account(email, password, sportsdbfile):
    conn = sqlite3.connect(sportsdbfile) 
    cursor = conn.cursor()

    cursor.execute("SELECT EMAIL FROM ACCOUNTS WHERE EMAIL = ?", (email,))
    exists = cursor.fetchone()

    if exists:  #uses fetchone to 'fetch' email if it already exists 
        print("Account linked with this email already exists") #if it exists this is printed to inform the user
        conn.close()
        return False
    else:
        cursor.execute("INSERT INTO ACCOUNTS(EMAIL, PASSWORD) VALUES(?, ?)", (email, password)) #if it doesnt exist inserts the account into the table 

    conn.commit()
    cursor.execute("SELECT email, password FROM ACCOUNTS")
    print("You have now made an account", cursor.fetchall()[-1]) #shows the user the account is made and also shows the account details by using fetch[-1] whcih fetches the most recent insert
    conn.close()

    return True