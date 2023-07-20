import sqlite3


def make_account(email, password):
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS ACCOUNTS(EMAIL VARCHAR(300), PASSWORD VARCHAR(300))'''
    cursor.execute(sql)

    cursor.execute("SELECT EMAIL FROM ACCOUNTS WHERE EMAIL = ?", (email,))
    exists = cursor.fetchone()

    if exists:
        print("Account linked with this email already exists")
        conn.close()
        return False
    else:
        cursor.execute(''' INSERT INTO ACCOUNTS(EMAIL, PASSWORD) VALUES(?,?)''', (email, password))
        

    conn.commit()
    cursor.execute("SELECT * FROM ACCOUNTS")
    print("You have now made an account",
        cursor.fethchall()[-1])
    conn.close()

    return True