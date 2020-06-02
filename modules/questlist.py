import os
import glob
import json
import configparser
import mysql.connector

def build(appVersion):
    resPath = "res/{}/raw/".format(appVersion) # Path to resource files from the APK.
    globPath = glob.glob(resPath + "questlist*.json") # Glob path to get all files that starts with questlist and ends with .json.

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
    queryInsertAllQuests = ''
    queryInsertAllStages = ''
    queryLineStarterQuest = 'INSERT INTO quest (shortName, questName, showInLog) VALUES '
    queryLineStarterStage = 'INSERT INTO stage (shortName, progress, logText, exp, finishesQuest) VALUES '
    isFinalFile = False

    # Iterate over all found files in the glob.
    for file in globPath:
        filename = os.path.basename(file) # The 'file' variable is a string with a path ('/raw/0.7.10/raw/questlist.json') and we need just the filename.

        # Determine whether the currently selected file is the last one in the 'globPath' list.
        if file == globPath[-1]:
            isFinalFile = True

        if filename != 'questlist_nondisplayed.json' and filename != 'questlist_debug.json': # These two files are not relavent to the end user and don't need to be included.

            # Open and load file's data into JSON object(s).
            f = open(file)
            fileData = json.load(f)
            f.close()

            # Iterate over the JSON object(s) for each quest.
            for quest in fileData:

                questName = quest['name'].replace("'", r"\'") # Needed to escape quotes for valid query strings.

                # Some quests do not get shown in the log. They are being skipped under the assumption that they will not help the end user.
                if 'showInLog' not in quest or quest['showInLog'] == 0:
                    continue

                # Check that the current quest is NOT the last quest in the final file in 'globPath'.
                if (isFinalFile and quest['id'] != fileData[-1]['id']) or not isFinalFile:
                    queryInsertAllQuests += '(\'%s\', \'%s\', %s), ' % (quest['id'], questName, quest['showInLog'])
                else:
                    queryInsertAllQuests += '(\'%s\', \'%s\', %s)' % (quest['id'], questName, quest['showInLog'])

                # Iterate over the quest for its stages.
                for stage in quest['stages']:
                    queryStagesToAdd = ''

                    # Some stages do not have this key. Set it to '' under the assumption that it won't be used.
                    if 'logText' not in stage:
                        logText = ''
                    else:
                        logText = stage['logText'].replace("'", r"\'") # Needed to escape quotes for valid query strings.

                    # Some stages are only for progression and do not give a reward. Set the value to NULL for sake of query.
                    if 'rewardExperience' not in stage:
                        rewardExp = 'null'
                    else:
                        rewardExp = stage['rewardExperience']

                    # If the stage is not the final stage for the quest, it will not have this key. Set it to 0 for sake of query.
                    if 'finishesQuest' not in stage:
                        finishesQuest = 0
                    else:
                        finishesQuest = 1

                    # Check whether the stage is not the final stage in the final file.
                    if (isFinalFile and stage['progress'] != quest['stages'][-1]['progress']) or not isFinalFile:
                        queryStagesToAdd += '(\'%s\', %s, \'%s\', %s, %s), ' % (quest['id'], stage['progress'], logText, rewardExp, finishesQuest)
                    else:
                        queryStagesToAdd += '(\'%s\', %s, \'%s\', %s, %s)' % (quest['id'], stage['progress'], logText, rewardExp, finishesQuest) # This will be the final VALUE line in the stage INSERT query.

                    queryInsertAllStages += queryStagesToAdd # Append the stage to the stage INSERT query.
        else:
            continue

    try:
        # pyperclip.copy(queryLineStarterStage + queryInsertAllStages + ';')
        cursor.execute(queryLineStarterQuest + queryInsertAllQuests + ';') # Run INSERT statement with all quests.
        cursor.execute(queryLineStarterStage + queryInsertAllStages + ';') # Run INSERT statement with all stages.
        con.commit()
        con.close()
        print("Finished building resources for Quests...")
    except mysql.connector.Error as err:
        print("MySQL Error: {}".format(err))