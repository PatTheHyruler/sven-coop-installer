import os
import re
import shutil
import sys
import tempfile
import winreg
from zipfile import ZipFile
import argparse
import ast



# Adding command line arguments with argparse
parser = argparse.ArgumentParser()

parser.add_argument("file", help="path to the zip file that you want to install", type=str)
parser.add_argument("-sp", "--svenpath", help="path to the directory where Sven Co-op is installed\nshould end with something like ...steamapps\\common\\Sven Co-op", type=str)
parser.add_argument("-i", "--iterations", help="how many iterations (of checking target file for necessary structure) to perform before quitting", type=int)

args = parser.parse_args()


# Setting default number of iterations and allowing it to be overridden by the optional iterations argument
if not args.iterations:
    maxiter = 4
else:
    maxiter = args.iterations





#function made by Rebane2001
def get_steam_path():
    """Get Steam install location from the Windows registry"""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             "SOFTWARE\\WOW6432Node\\Valve\\Steam")
        value = winreg.QueryValueEx(key, "InstallPath")[0]
        return value
    except:
        raise Exception("Couldn't locate Steam")

#function mostly made by Rebane2001
def get_game_path(steampath):
    """Scan through every Steam library and try to find a Sven installation"""
    try:
        gamepaths = [f"{steampath}"]
        with open(f"{steampath}\\steamapps\\libraryfolders.vdf", "r") as f:
            for l in f:
                # If is an absolute path with a drive letter (eg "D:\\Games")
                if ":\\\\" in l:
                    gamepaths.append(ast.literal_eval("\""+l.split("\t")[-1][1:-2]+"\""))
        for gamepath in gamepaths:
            if (os.path.isfile(f"{gamepath}\\steamapps\\appmanifest_225840.acf")):
                return f"{gamepath}\\steamapps\\common\\Sven Co-op\\"
        raise Exception("Couldn't locate Sven Co-op")
    except:
        raise Exception("Couldn't locate Sven Co-op")


if args.svenpath:
    path = args.svenpath
else:
    steampath = get_steam_path()
    path = get_game_path(steampath)

sven_dst = f"{path}\\svencoop_addon"

# Creating svencoop_addon in path if it doesn't exist there yet
try:
    os.mkdir(sven_dst)
except FileExistsError:
    pass



# Defining a function that iterates through the files and folders in the temp directory, checks them for correct file structure, and if it finds a match, extracts that to svencoop_addon
# temp = current directory that the function is operating in
def install(temp, iteration):
    iteration += 1
    if os.path.isdir(temp+"\\maps"):
        for f in os.listdir(temp):
            if os.path.exists(f"{sven_dst}\\{f}"):
                shutil.rmtree(f"{sven_dst}\\{f}")
            shutil.move(f"{temp}\\{f}", sven_dst)
    elif iteration <= maxiter:
        for f in os.listdir(temp):
                try:
                    install(f"{temp}\\{f}", iteration)
                except:
                    continue
    else:
        return


# Creating a temporary folder to store extracted files in
temp = tempfile.TemporaryDirectory(None,"sven co-op map installer.",tempfile.gettempdir()).name


# Checking if the target file is a zip file
# if it is, extracting its contents to the temp folder and running the install function
try:    
    if re.match(r".+\.zip$", args.file, re.IGNORECASE):
        zip = ZipFile(args.file, "r")
        zip.extractall(temp)
        install(temp, 0)
    else:
        input("Expected a .zip file as input")
except:
    raise
finally:
    # Deleting the temp folder (not sure if this is even needed)
    shutil.rmtree(temp)