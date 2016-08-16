#!/usr/bin/python
import os
import pickle
import requests
import shutil
import sys

home = sys.argv[1]
if home[len(home)-1] != "/":
    home = home + "/"
srcDir = home + "src"
photosDir = home + "photos"
historyDir = photosDir + "/history"
logDir = home + "logs"
print("Creating Directories...")
if not os.path.exists(srcDir):
    os.makedirs(srcDir)
if not os.path.exists(photosDir):
    os.makedirs(photosDir)
if not os.path.exists(historyDir):
    os.makedirs(historyDir)
if not os.path.exists(logDir):
    os.makedirs(logDir)

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
print("Creating Configuration...")
conf={  "screenWidth" : width,
        "screenHeight" : height,
        "current" : ""  }
pickle.dump(conf, open("conf.info", "wb"))

SRCLIST = ["runner", "connection", "imageAnalyzer", "redditHTML"]

def downloadAndSaveSrcFile(name, directory):
    r = requests.get("https://raw.githubusercontent.com/pwteneyck/redditwallpaper/master/src/" + name)
    that = open(directory + name, "w")
    that.write(r.text)

for thing in SRCLIST:
    downloadAndSaveSrcFile(thing + ".py", srcDir)

