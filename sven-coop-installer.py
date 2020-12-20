import os
import re
import shutil
import sys
import tempfile
import winreg
import argparse
import ast
#required for os detection
import platform

# Archive support
import zipfile
import tarfile
# NOT INCLUDED IN STANDARD PYTHON LIBRARY:
import py7zr
import rarfile



# Adding command line arguments with argparse
parser = argparse.ArgumentParser()

parser.add_argument("file", help="path to the archive (probably .zip) file(s) that you want to install", type=str, nargs='+')
parser.add_argument("-sp", "--svenpath", help="path to the directory where Sven Co-op is installed.\n Should end with something like ...steamapps\\common\\Sven Co-op", type=str)
parser.add_argument("-i", "--iterations", help="how many iterations (of checking target file for necessary structure) to perform before quitting", type=int)

args = parser.parse_args()


# Setting default number of iterations and allowing it to be overridden by the optional iterations argument
if not args.iterations:
    maxiter = 4
else:
    maxiter = args.iterations





#function mostly made by Rebane2001
def get_steam_path():
    
    if platform.system() == "Windows":
        """Get Steam install location from the Windows registry"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                "SOFTWARE\\WOW6432Node\\Valve\\Steam")
            value = winreg.QueryValueEx(key, "InstallPath")[0]
            return value
        except:
            input("Couldn't locate Steam. Press Enter to quit.")
    elif platform.system() == "Linux":
        print("Automatic sven location detection not supported on Linux, sorry.")

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
        input("Couldn't locate Sven Co-op. Press Enter to quit.")


if args.svenpath:
    path = args.svenpath
else:
    steampath = get_steam_path()
    path = get_game_path(steampath)

sven_dst = f"{path}svencoop_addon"

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
        # walk keeps track of what cycle we're in in the following for loop
        walk = -1
        for root, dirs, files in os.walk(temp):
            walk+=1
            if root==temp:
                pass
            else:
                try:
                    os.makedirs(root.replace(temp, sven_dst))
                except FileExistsError:
                    pass

            for item in files:
                if walk == 0:
                    shutil.copy(f"{temp}\\{item}", sven_dst)
                else:
                    src = os.path.join(root, item)
                    dst = src.replace(temp, sven_dst)
                    shutil.copy(src, dst)

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

# Checking if the target file is a valid input archive
# if it is, extracting its contents to the temp folder and running the install function
for file in args.file:
    try:    
        if zipfile.is_zipfile(file):
            archive = zipfile.ZipFile(file)
        elif re.match(r".+\.7z$", file, re.IGNORECASE):
            archive = py7zr.SevenZipFile(file)
        elif tarfile.is_tarfile(file):
            archive = tarfile.open(file)
        elif rarfile.is_rarfile(file):
            archive = rarfile.RarFile(file)
        else:
            archive = False
            raise Exception("Unsupported input archive.")
        archive.extractall(temp)
        install(temp, 0)
    except:
        print(f"Failed on {file}.\nTrying next file / quitting if no other files given.")
    finally:
        if os.path.isdir(temp):
            shutil.rmtree(temp)