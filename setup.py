#!/usr/bin/python
import os
import pickle
import shutil
import sys

home = sys.argv[1]
if home[len(home)-1] != "/":
    home = home + "/"
directory = home + "redditwallpaper/src"
print("Creating Directories...")
if not os.path.exists(directory):
    os.makedirs(directory)

print("Copying Source...")
srcDir = "./src/"
srcFiles = os.listdir(srcDir)
for fileName in srcFiles:
    fullName = os.path.join(srcDir, fileName)
    if os.path.isfile(fullName):
        shutil.copy(fullName, directory)

# get screen width and height
print("Gathering System Specifications...")
if os.name == "posix":
    sysWidth = os.popen("system_profiler SPDisplaysDataType | grep Resolution | grep -Eoi \"([0-9]+) x ([0-9]+)\" | cut \
            -d ' ' -f 1").read()
    sysHeight = os.popen("system_profiler SPDisplaysDataType | grep Resolution | grep -Eoi \"([0-9]+) x ([0-9]+)\" | cut \
            -d ' ' -f 3").read()
elif os.name == 'nt':
    # TODO get resolution for Windows
    print("Not implemented for Windows yet :|")
# if there are multiple monitors, just use the resolution for the primary one
# TODO figure something out for multiple monitors?  IDK.
width = sysWidth.splitlines()[0]
height = sysHeight.splitlines()[0]

# write screen width and height to configuration file
conf={  "screenWidth" : width,
        "screenHeight" : height,
        "current" : ""  }
pickle.dump(conf, open("conf.info", "wb"))
