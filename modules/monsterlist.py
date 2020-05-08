import os
import glob

def build(appVersion):
    count = 0
    path = "res/{}/raw/".format(appVersion)
    for file in glob.glob(path + "monsterlist*.json"):
        count += 1

    print("Monsterlist Files Found: " + str(count))
    print("Finished building resources for Monsters.")