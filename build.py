#!/usr/bin/env python3
import configparser, mysql.connector
from modules import questlist, monsterlist, itemlist, itemcategories, worldmap

# Update this to reflect the version of Andor's Trail we want to use.
# Place the 'res' folder from the APK into the versions folder with the following structure: versions/0.7.13/
appVersion = '0.7.13'
resPath = "versions\\{}\\res\\".format(appVersion)

# Database connection
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

# Run each module and generate database records.
# questlist.build(resPath, "questlist*.json", config, con, cursor)
# monsterlist.build(resPath, "monsterlist*.json", config, con, cursor)
# itemlist.build(appVersion)
# itemcategories.build(appVersion)
worldmap.generateMapImages(resPath + "xml\\", "*.tmx")

# Done!
print("All resources have been built!")