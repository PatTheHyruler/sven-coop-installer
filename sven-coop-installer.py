#Importing stuff, obviously
import os
import pathlib
import re
import shutil
import sys
from zipfile import ZipFile

#Creating readme file
with open("readme.txt",'w',encoding = 'utf-8') as r:
    r.write("This program was created by Patrick McRoof (PatTheHyruler#5698 on Discord).\n")
    r.write("You can turn to me if you have issues, though please try to figure things out on your own first, if it seems at all possible\n")
    r.write("\n\nSimple instructions: put the program in the same folder as your map (.zip) files, run the program and do what it tells you (if it tells you to do something).\n")
    r.write("\nThis program assumes that you are running Windows 10.\n\n\n")
    r.write("This program will look at all zip files in the same directory as itself, and check with some very rudimentary logic if the file structure within the zip file is correct.\n")
    r.write("(For those who care, it checks if there is anything called \"maps\" in the zip file or any folder in the zip file (it does not check in any folders inside those folders though), and extracts the contents of the directory containing the folder (or file, but it shouldn't be a file) named \"maps\" to the svencoop_addon folder.)\n")

    r.write("You will be asked to paste certain directory paths to certain text files. If the program doesn't work, that is the first thing I recommend you double and triple check.")
    r.write("\n\nIf you want the program to check for map zip files in another directory, not the one it's located in, you need to create a file named \"map_ingest.txt\" in the same folder as the program and enter your desired map-checking directory's path there.")
    r.write("\n\n\n\n2020-05-04")

#Checking if a txt file with the path to sven exists
try:
    sven = open("sven_path.txt", "r")
except FileNotFoundError:
    sven = open("sven_path.txt", "w")
    sven.close()
    sven = open("sven_path.txt", "r")
sven_dst = sven.readline().strip()
sven.close()

#This makes it so things don't close, look at following code to understand
exit = False

#Adding a thing to check if the sven path file is empty or not, and prompting the user to stop it from being empty if it is empty
if len(sven_dst) == 0:
    print("Please enter the path to your Sven Co-Op folder (something like D:\\SteamLibrary\\steamapps\\common\\Sven Co-op) in the sven_path.txt file.\n")
    i = input("If you need help with that, type Y (and press Enter). Type anything else to quit the program.\n")
    try:
        if i=="Y" or i=="y":
            print("\n\n(Assuming you have Sven Co-Op on Steam) go to your library (in Steam),\n\nfind Sven Co-Op,\n\nright click on it in the list,\n\ngo to \"Manage → Browse local files\".\n\nNow a file explorer window should have popped up.\n\nCopy the path (near the top of the window),\n\npaste it into sven_path.txt\n\nand save sven_path.txt.")
            input("\n\nIf this didn't help you, you're on your own, sorry. Press Enter to quit the program.")
            exit = True
        else:
            exit = True
    finally:
        exit = True
#Doing what the user wants
if exit:
    sys.exit()

#Creating a variable to store the path of the svencoop_addon folder
sven_dst = sven_dst+"\\svencoop_addon"

#Getting the path of where this program is being executed from
path = pathlib.Path(__file__).parent.absolute()

#Adding an option for people who read the readme to have a custom map ingest folder
if "map_ingest.txt" in os.listdir(path):
    with open("map_ingest.txt", "r") as m:
        path = m.readline().strip()

#Storing a list of all the contents (without entering directories) in the map ingest folder as variable c_list
c_list = os.listdir(path)
#Creating a temporary folder to do stuff in
temp = f"{path}\\temp"

#regex pattern to match strings ending in ".zip" (any capitalization)
pattern = r".+\.[Zz][Ii][Pp]$"

#filtering all the non-zip files out of c_list
z_list = []
for i in c_list:
    if re.match(pattern, i):
        z_list.append(i)

#Creating a function for checking for correct folder structure (very rudimentary logic) and move all the contents of the hopefully correct directory to svencoop_addon
def install(temp, iteration, i):
    iteration += 1
    if "maps" in os.listdir(temp):
        for f in os.listdir(temp):
            shutil.move(f"{temp}\\{f}", f"{sven_dst}\\{f}")
    else:
        print(f"Couldn't find correct file structure indicator on iteration {iteration} through {i}\nType Q to quit on {i} or anything else to continue\n")
        quitcheck = input("")
        if quitcheck=="Q" or quitcheck=="q":
            return
        else:
            for file in os.listdir(temp):
                try:
                    install(f"{temp}\\{file}", iteration, f"{i}\\{file}")
                except:
                    continue

#Iterating through the zip files, extracting them to the temp folder and passing them into the previously created install function
for i in z_list:
    iteration = 0
    zip = ZipFile(f"{path}\\{i}", "r")
    zip.extractall(temp)
    install(temp, iteration, i)

try:
    #Deleting the temp folder
    shutil.rmtree(temp)
finally:
    sys.exit()