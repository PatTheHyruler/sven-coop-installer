#!/bin/bash

# Script to run the sven-coop-installer.py file on Linux
# with the path to the Sven Coop installation already entered as an argument.

# Insert the path to your Sven Co-op installation folder. It should end with something like this: ...steamapps/common/Sven Co-op
svenpath=""
python3 sven-coop-installer.py -sp $svenpath