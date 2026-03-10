import sqlite3

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
id INTEGER PRIMARY KEY,
account TEXT,
password TEXT
)
""")

def add_password(account, password):
    cursor.execute(
        "INSERT INTO passwords(account,password) VALUES(?,?)",
        (account, password)
    )
    conn.commit()


def get_passwords():
    cursor.execute("SELECT * FROM passwords")
    return cursor.fetchall()


def delete_password(account):

    cursor.execute("DELETE FROM passwords WHERE account=?", (account,))
    conn.commit()

    # rowcount tells how many rows were affected
    if cursor.rowcount == 0:
        return False
    else:
        return True