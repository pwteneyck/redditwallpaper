import os
import pickle

#configuration = open('conf.info', 'w')
screenWidth = int(os.system("system_profiler SPDisplaysDataType | grep Resolution | grep -Eoi \"([0-9]+) x ([0-9]+)\" | cut -d ' ' -f 1"))
screenHeight = int(os.system("system_profiler SPDisplaysDataType | grep Resolution | grep -Eoi \"([0-9]+) x ([0-9]+)\" | cut -d ' ' -f 3"))

conf={"screenWidth" : screenWidth, "screenHeight" : screenHeight}
pickle.dump(conf, open("conf.info", "wb"))
