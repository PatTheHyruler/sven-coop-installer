import os
import re
import shutil
import sys
import tempfile
import winreg
from zipfile import ZipFile
import argparse


# Adding command line arguments with argparse
parser = argparse.ArgumentParser()

parser.add_argument("file", help="path to the file that you want to install", type=str)
parser.add_argument("-sp", "--svenpath", help="path to the directory where Sven Co-op is installed\nshould end with something like ...steamapps\\common\\Sven Co-op", type=str)
parser.add_argument("-i", "--iterations", help="how many iterations (of checking target file for necessary structure) to perform before quitting", type=int)

args = parser.parse_args()


# Setting default number of iterations and allowing it to be overridden by the optional iterations argument
if not args.iterations:
    maxiter = 4
else:
    maxiter = args.iterations


# Checking if a svenpath.txt file exists in the current working directory (which should be where the program was run), and if it does, reading the Sven Co-op path from there
svenpath = f"{os.getcwd()}\\svenpath.txt"
if os.path.isfile(svenpath):
    with open(svenpath, "r") as f:
        sven_dst = f.readline().strip()+"\\svencoop_addon"

# Checking if Sven Co-op is installed in any of the default Sven Co-op install locations on Windows
# and if it can't be found, prompting the user to provide a path to Sven Co-op
if not args.svenpath and not os.path.isfile(svenpath):
    try:
        steam_path = winreg.EnumValue(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Valve\\Steam"),1)[1]
        steam32 = True
    except:
        steam32 = False
    try:
        steam_path = winreg.EnumValue(winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Valve\\Steam"),1)[1]
        steam64 = True
    except:
        steam64 = False
    if steam32 == False and steam64 == False:
        input("Couldn't find path to svencoop_addon.\nUse -sp [path to sven] to specify Sven Co-op install folder.")
        #SVEN PATH PROMPT
        sys.exit()
    else:
        sven_dst = f"{steam_path}\\steamapps\\common\\Sven Co-op\\svencoop_addon"
# The optional command line argument --svenpath overrides every other source for finding Sven Co-op
elif args.svenpath:
    sven_dst = f"{args.svenpath}\\svencoop_addon"

# Checking if the sven_dst directory exists and if not, prompting the user to provide a path to Sven Co-op
if not os.path.isdir(sven_dst):
            input("Couldn't find path to svencoop_addon.\nUse -sp [path to sven] to specify Sven Co-op install folder.")
            #SVEN PATH PROMPT
            sys.exit()


# Creating a temporary folder to store extracted files in
temp = tempfile.TemporaryDirectory(None,"sven co-op map installer.",tempfile.gettempdir()).name



# Defining a function that iterates through the files and folders in the temp directory, checks them for correct file structure, and if it finds a match, extracts that to svencoop_addon
# temp = current directory that the function is operating in
# i = item that function is currently being run on (folder or file)
def install(temp, iteration):
    iteration += 1
    if os.path.isdir(temp+"\\maps"):
        for f in os.listdir(temp):
            shutil.move(f"{temp}\\{f}", f"{sven_dst}\\{f}")
    elif iteration <= maxiter:
        for file in os.listdir(temp):
                try:
                    install(f"{temp}\\{file}", iteration)
                except:
                    continue
    else:
        return

# Checking if the target file is a zip file
# if it is, extracting its contents to the temp folder and running the install function
if re.match(r".+\.zip$", args.file, re.IGNORECASE):
    zip = ZipFile(args.file, "r")
    zip.extractall(temp)
    install(temp, 0)
else:
    input("Expected a .zip file as input")

# Deleting the temp folder (not sure if this is even needed)
temp.cleanup()