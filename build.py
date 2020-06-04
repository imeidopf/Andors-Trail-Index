#!/usr/bin/env python3
from modules import questlist, monsterlist, itemlist, itemcategories

# Update this to reflect the version of Andor's Trail we want to use.
# Place the xml and raw files inside the res folder. E.g. res/0.7.10
appVersion = '0.7.10'

# Run each module and build out the database material.
questlist.build(appVersion)
#monsterlist.build(appVersion)
#itemlist.build(appVersion)
#itemcategories.build(appVersion)

# Done!
print("All resources have been built!")