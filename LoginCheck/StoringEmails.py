import sqlite3

def make_account(email, password, sportsdbfile):
    conn = sqlite3.connect(sportsdbfile) 
    cursor = conn.cursor()

    cursor.execute("SELECT EMAIL FROM ACCOUNTS WHERE EMAIL = ?", (email,))
    exists = cursor.fetchone()

    if exists:
        print("Account linked with this email already exists")
        conn.close()
        return False
    else:
        cursor.execute("INSERT INTO ACCOUNTS(EMAIL, PASSWORD) VALUES(?, ?)", (email, password))

    conn.commit()
    cursor.execute("SELECT email, password FROM ACCOUNTS")
    print("You have now made an account", cursor.fetchall()[-1])
    conn.close()

    return True
