# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python

import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE personal")

print("Done!")
