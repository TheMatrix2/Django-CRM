# sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
# sudo apt-get install mysql-client libssl-dev
# pip install -r requirements.txt

import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE personal")

print("Done!")
