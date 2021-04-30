import os, glob, json, mysql.connector

def build(resPath, globFilter, config, con, cursor):
    globPath = glob.glob(resPath + globFilter) # Glob path to get all files that starts with questlist and ends with .json.
    print("Questlist files found: " + str(len(globPath)))

    # Generic query variables used to build out the MySQL queries.
    queryInsertAllQuests = ''
    queryInsertAllStages = ''
    queryLineStarterQuest = 'INSERT INTO quest (questShortName, questName) VALUES '
    queryLineStarterStage = 'INSERT INTO stage (questShortName, progress, logText, rewardExp, finishesQuest) VALUES '
    isFinalFile = False

    print('Starting Quest data generation...')

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
                    queryInsertAllQuests += '(\'%s\', \'%s\'), ' % (quest['id'], questName)
                else:
                    queryInsertAllQuests += '(\'%s\', \'%s\')' % (quest['id'], questName)

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
                    if 'finishesQuest' not in stage or stage['finishesQuest'] == 0:
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
        cursor.execute(queryLineStarterQuest + queryInsertAllQuests + 'ON DUPLICATE KEY UPDATE questID=questID;') # Run INSERT statement with all quests.
        print("Inserting Quest list into database...")
        cursor.execute("TRUNCATE TABLE stage;") # Needed because a method to prevent duplicate stages hasn't been created yet.
        cursor.execute(queryLineStarterStage + queryInsertAllStages + ';') # Run INSERT statement with all stages.
        print("Inserting Stage list into database...")
        con.commit()
        con.close()
        print("Finished Quest data generation...")
    except mysql.connector.Error as err:
        print("MySQL Error: {}".format(err))