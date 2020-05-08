import os
import glob

def build():
    count = 0
    path = "res/0.7.10/raw/"
    for file in glob.glob(path + "questlist*.json"):
        count += 1

    print("Questlist Files Found: " + str(count))