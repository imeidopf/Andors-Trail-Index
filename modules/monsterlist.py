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
    masterDict = {}

    print('Starting Monster data generation...')

    # Iterate over all found files in the glob.
    for file in globPath:
        if file == globPath[-1]:
            isFileFile = True

        f = open(file)
        fileData = json.load(f)
        f.close()
        
        for monster in fileData:
            masterDict.update(monster)

    #print(masterDict.keys())
    print(json.dumps(masterDict, indent=4))
    print("Finished Monster data generation...")