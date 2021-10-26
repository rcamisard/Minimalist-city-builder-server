import os
import psycopg2
import json

DATABASE_URL = os.environ['DATABASE_URL']

def createTables():
    dbConnection = psycopg2.connect(DATABASE_URL, sslmode='require')

    dbCursor = dbConnection.cursor()
    dbCursor.execute("CREATE TABLE IF NOT EXISTS CLASSEMENTS (USERNAME text, POINTS int)")
    dbConnection.commit()
    dbConnection.close()
def getClassements():
    dbConnection = psycopg2.connect(DATABASE_URL, sslmode='require')
    dbCursor = dbConnection.cursor()
    dbCursor.execute("SELECT USERNAME, POINTS FROM CLASSEMENTS ORDER BY POINTS DESC LIMIT 100")

    res = json.dumps(dbCursor.fetchall())
    dbConnection.close()
    # On doit stocker la reponse avant de fermer la connexion à la base
    return res

def insertClassement(username, score):
    dbConnection = psycopg2.connect(DATABASE_URL, sslmode='require')
    dbCursor = dbConnection.cursor()

    dbCursor.execute("INSERT INTO %s VALUES (%%s,%%s)" % "CLASSEMENTS", [username, score])
    dbConnection.commit()
    dbConnection.close()