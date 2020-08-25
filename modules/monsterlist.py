import os
import glob
import json
import configparser
import mysql.connector

def build(appVersion):
    resPath = "res/{}/raw/".format(appVersion) # Path to resource files from the APK.
    globPath = glob.glob(resPath + "monsterlist*.json") # Glob path to get all files that starts with monsterlist and ends with .json.

    # Setup the database connection.
    config = configparser.ConfigParser()
    config.read('configs/db.ini') # This file will hold your database connection information. THIS FILE IS NOT INCLUDED AS OF RIGHT NOW!
    con = mysql.connector.connect(
        host = config.get('DATABASE', 'host'),
        db = config.get('DATABASE', 'db'),
        user = config.get('DATABASE', 'user'),
        passwd = config.get('DATABASE', 'pwd')
    )
    cursor = con.cursor()

    # Generic query variables used to build out the MySQL queries.
    queryInsertAllMonsters = ''
    queryLineStarterMonster = ''
    isFinalFile = False
    count = 0

    print('Starting Monster data generation...')

    # Iterate over all found files in the glob.
    for file in globPath:
        count += 1

    print("Monsterlist Files Found: " + str(count))
    print("Finished Monster data generation...")