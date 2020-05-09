import os, glob, json

def build(appVersion):
    count = 0
    path = "res/{}/raw/".format(appVersion)

    for file in glob.glob(path + "questlist*.json"):
        filename = os.path.basename(file)
        if filename != 'questlist_nondisplayed.json' and filename != 'questlist_debug.json':
            f = open(file)
            data = json.load(f)
            for quest in data:
                print("File: " + filename + "\r\n     " + quest['name'])
                for stage in quest['stages']:
                    if 'logText' in stage:
                        print("          " + str(stage['progress']) + "% | " + stage['logText'])
                    else:
                        print("          " + str(stage['progress']) + "%")
        else:
            print('Skipped File: ' + filename)
            continue
        count += 1

    print("Questlist Files Found: " + str(count))
    print("Finished building resources for Quests.")