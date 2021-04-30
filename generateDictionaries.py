import os, glob, json, mysql.connector

appVersion = "0.7.13"
resPath = "versions/{}/raw/".format(appVersion)

dictQuests = {}
dictMonsters = {}

globQuests = glob.glob(resPath + "questlist*.json")
globMonsters = glob.glob(resPath + "monsterlist*.json")

for file in globQuests:
    f = open(file)
    fileData = json.load(f)
    f.close()
    
    for quest in fileData:
        dictQuests.update(quest)

for file in globMonsters:
    f = open(file)
    fileData = json.load(f)
    f.close()
    
    for monster in fileData:
        dictMonsters.update(monster)

# print(dictMonsters.keys())
# print(json.dumps(dictMonsters, indent=4))