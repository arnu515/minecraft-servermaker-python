#
#   Minecraft Server Maker
#   Using Python
#   By Aarnav Pai
#
#   All files obtained from https://yivesmirror.com/
#
#   Feel free to change the code or fork it on GitHub!
#   https://github.com/arnu515/minecraft-servermaker-python/
#


import os, platform
from time import sleep
from tkinter import filedialog, Tk
import requests, json

def getVersions():

    get = requests.get("https://yivesmirror.com/api/list/paper")
    versionJson = get.content
    versionList = json.loads(versionJson)

    return versionList

def getInfo(version):
    
    get = requests.get("https://yivesmirror.com/api/file/paper/" + version)
    infoJson = get.content
    infoDict = json.loads(infoJson)

    return infoDict

def getFile(path, version, infoDict, oS):

    get = requests.get(infoDict["direct_link"])
    if oS == "Windows":
        location = path + "\\paper.jar"
    else:
        location = path + "/paper.jar"
    with open(location, "wb") as f:
        f.write(get.content)

def cl(): #Function to clear the screen
    if platform.system() == "Windows": #Checks if the OS is windows
        os.system("cls") #Executes cls command via cmdprompt
    else:
        os.system("clear")

sleep(0.5)
cl()

print("-----")
print("\nWelcome to the installer!")

#Getting server location
while True: 
    print("Press enter to choose the location of your server!")
    x1 = input("")

    win = Tk() #Creating a window and removing it so empty frame doesn't appear when using filedialog
    win.withdraw()

    location = filedialog.askdirectory(initialdir=os.getcwd()) #Open a file explorer and ask for directory
    print("\nOk, choosing {}. Make sure there are no files in it!".format(location))
    x2 = input("Go with this directory? (y=yes/anything else=no): ")
    if "y" in x2:
        break
    else:
        print("Pick your directory again!")
        sleep(0.5)
        cl()
        continue

#Getting the list of paper versions
sleep(1)
cl()
print("Getting the list of available Paper versions...")
versionList = getVersions() #Getting the list of paper versions

#Making the user select version
while True: 
    print("\nVersions:")
    i = 1
    for item in versionList: #Print all versions
        print(str(i) + ". " + item)
        i += 1
    print("\nPick one by entering its exact name (For example: Paper-1.15.2-b87.jar)")
    x3 = input()
    if x3 in versionList: #Get the version info
        print("\nGetting information about {} ...".format(x3))
        info = getInfo(x3)
        print("\nSize:", info["size_human"])
        print("Minecraft Version:", info["mc_version"])
        print("Date last updated:", info["date_human"])
        print("Download from:", info["grab_link"])
        x4 = input("\nConfirm this version? (y=yes/anything else=no): ")
        if "y" in x4:
            print("\nDownloading {} from {} and saving it as {}/paper.jar".format(x3, info["direct_link"], location))
            getFile(location, x3, info, platform.system())
            print("Successfully saved paper.jar!")
            break
        else:
            print("Ok, choose another version")
            sleep(1)
            cl()
            continue
    else:
        print("Invalid version! Enter its exact name!")
        print("Reprinting all the versions...")
        sleep(0.5)
        cl()
        continue

#Making other files
sleep(2)
cl()
maxRam = input("Enter the max ram for your server: ")
minRam = input("Enter the starting ram for your server: ")
optParam = input("Enter any optional parameters: ")

startBat = "java -Xms" + minRam + " -Xmx" + maxRam + " " + optParam + " -jar paper.jar"
if platform.system() == "Windows":
    pathBat = location + "\\start.bat"
else:
    pathBat = location + "/start.sh"
with open(pathBat, "w") as f:
    f.write(startBat)
if platform.system() != "Windows":
    os.system("chmod +x start.sh")

if platform.system() == "Windows":
    pathEULA = location + "\\eula.txt"
else:
    pathEULA = location + "/eula.txt"
with open(pathEULA, "w") as f:
    f.write("eula=true")

print("\nCreated two files: start.bat/sh and eula.txt")
print("Your server is now ready to start! Enjoy..")
print("Bye!")
sleep(5)
cl()
