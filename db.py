import sqlite3
import json
from sqlite3 import Error


def createTables(dbFile):
    dbConnection = sqlite3.connect(dbFile)

    dbCursor = dbConnection.cursor()
    dbCursor.execute('''CREATE TABLE IF NOT EXISTS CLASSEMENTS
                   (USERNAME, POINTS, CREATION_DATE)''')

    dbConnection.close()

def getClassements(dbFile):

    dbConnection = sqlite3.connect(dbFile)
    dbCursor = dbConnection.cursor()

    dbCursor.execute("SELECT USERNAME, POINTS FROM CLASSEMENTS ORDER BY POINTS DESC")
    res = json.dumps(dbCursor.fetchall())
    dbConnection.close()
    # On doit stocker la reponse avant de fermer la connexion à la base
    return res

def insertClassement(dbFile):
    dbConnection = sqlite3.connect(dbFile)
    dbCursor = dbConnection.cursor()

    dbCursor.execute("INSERT INTO CLASSEMENTS VALUES (?,?, date('now'))", username, points)
    dbConnection.commit()

    dbConnection.close()
