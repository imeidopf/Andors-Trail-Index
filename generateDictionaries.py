import os, glob, json, mysql.connector

appVersion = "0.7.13"
resPath = "versions/{}/raw/".format(appVersion)

dictQuests = {}
dictMonsters = {}
dictConditions = {}
dictItems = {}
dictDrops = {}

globQuests = glob.glob(resPath + "questlist*.json")
globMonsters = glob.glob(resPath + "monsterlist*.json")
globConditions = glob.glob(resPath + "actorconditions*.json")
globItems = glob.glob(resPath + "itemlist*.json")
globDrops = glob.glob(resPath + "droplists*.json")

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

for file in globConditions:
    f = open(file)
    fileData = json.load(f)
    f.close()
    
    for condition in fileData:
        dictConditions.update(condition)

for file in globItems:
    f = open(file)
    fileData = json.load(f)
    f.close()
    
    for item in fileData:
        dictItems.update(item)

for file in globDrops:
    f = open(file)
    fileData = json.load(f)
    f.close()
    
    for drop in fileData:
        dictDrops.update(drop)

file_quest = open("dictionary_quests.json", "w")
file_quest.write(json.dumps(dictQuests))
file_quest.close()

file_monster = open("dictionary_monsters.json", "w")
file_monster.write(json.dumps(dictMonsters))
file_monster.close()

file_monster = open("dictionary_conditions.json", "w")
file_monster.write(json.dumps(dictConditions))
file_monster.close()

file_monster = open("dictionary_items.json", "w")
file_monster.write(json.dumps(dictItems))
file_monster.close()

file_monster = open("dictionary_drops.json", "w")
file_monster.write(json.dumps(dictDrops))
file_monster.close()

# print(dictQuests.keys())
# print(json.dumps(dictMonsters, indent=4))