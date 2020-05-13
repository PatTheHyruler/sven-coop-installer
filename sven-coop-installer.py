import os
import pathlib
import re
import shutil
import sys

with open("readme.txt",'w',encoding = 'utf-8') as r:
    r.write("This program was created by Patrick McRoof (PatTheHyruler#5698 on Discord).\n")
    r.write("You can turn to me if you have issues, though please try to figure things out on your own first, if it seems at all possible\n")
    r.write("\n\nSimple instructions: put the program in the same folder as your map (.zip) files, run the program and do what it tells you (if it tells you to do something).\n")
    r.write("\nThis program assumes that you are running Windows 10, and that you have the 7-Zip archive manager program installed.\n\n\n")
    r.write("This program will look at all zip files in the same directory as itself, and check with some very rudimentary logic if the file structure within the zip file is correct.\n")
    r.write("(For those who care, it checks if there is anything called \"maps\" in the zip file or any folder in the zip file (it does not check in any folders inside those folders though), and extracts the contents of the directory containing the folder (or file, but it shouldn't be a file) named \"maps\" to the svencoop_addon folder.)\n")

    r.write("You will be asked to paste certain directory paths to certain text files. If the program doesn't work, that is the first thing I recommend you double and triple check.")
    r.write("\n\nIf you want the program to check for map zip files in another directory, not the one it's located in, you need to create a file named \"map_ingest.txt\" in the same folder as the program and enter your desired map-checking directory's path there.")
    r.write("\n\n\n\n2020-05-04")
    

try:
    zipper = open("zipper_path.txt", "r")
except FileNotFoundError:
    zipper = open("zipper_path.txt", "w")
    zipper.close()
    zipper = open("zipper_path.txt", "r")
zipper_path = zipper.readline()
zipper.close()

try:
    sven = open("sven_path.txt", "r")
except FileNotFoundError:
    sven = open("sven_path.txt", "w")
    sven.close()
    sven = open("sven_path.txt", "r")
sven_dst = sven.readline()
sven.close()

exit = False

if len(zipper_path) == 0:
    print("Please enter the path to your 7-zip executable (something like C:\\Program Files\\7-Zip) in the zipper_path.txt file.")
    input("\nPress Enter to continue/quit\n\n")
    exit = True

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

if exit:
    sys.exit()

sven_dst = sven_dst+"\\svencoop_addon"

path = pathlib.Path(__file__).parent.absolute()

c_list = os.listdir(path)

if "map_ingest.txt" in c_list:
    with open("map_ingest.txt", "r") as m:
        path = m.readline()

c_list = os.listdir(path)
temp = f"{path}\\temp"

pattern = r".+\.[Zz][Ii][Pp]$"

z_list = []
for i in c_list:
    if re.match(pattern, i):
        z_list.append(i)

try:
    os.system(f"cd {zipper_path}")
    for i in z_list:
        os.system(f"7z x \"{path}\\{i}\" -o\"{temp}\" -aoa")
        if "maps" in os.listdir(temp):
            for f in os.listdir(temp):
                shutil.move(f"{temp}\\{f}", f"{sven_dst}\\{f}")
        else:
            for l in os.listdir(temp):
                path_n = temp+"\\"+l
                try:
                    if "maps" in os.listdir(path_n):
                        for f in os.listdir(path_n):
                            shutil.move(f"{path_n}\\{f}", f"{sven_dst}\\{f}")
                except:
                    continue
except:
    raise

try:
    shutil.rmtree(temp)
finally:
    sys.exit()