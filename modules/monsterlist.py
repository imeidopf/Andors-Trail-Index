import os, glob, json, mysql.connector

def build(resPath, globFilter, config, con, cursor):
    globPath = glob.glob(resPath + globFilter) # Glob path to get all files that starts with monsterlist and ends with .json.
    print("Monsterlist files found: " + str(len(globPath)))

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
    #print(json.dumps(masterDict, indent=4))
    print("Finished Monster data generation...")