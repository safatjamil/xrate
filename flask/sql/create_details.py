import sqlite3

connection = sqlite3.connect("xrate.db")
cur = connection.cursor()
cur.execute("INSERT INTO details (last_updated, timezone) 
             VALUES ('None', 'None')"
           )
connection.commit()
connection.close()
