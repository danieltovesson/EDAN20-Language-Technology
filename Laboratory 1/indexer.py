from sys import argv
import os
import re
import pickle

def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

dir = argv[1]
file_names = get_files(dir, ".txt")
matches = {}

for file_name in file_names:
    file_object  = open(dir+"/"+file_name).read()
    for match in re.finditer(r"\w+", file_object.lower()):
        if match.group(0) in matches:
            matches[match.group(0)].append(match.start())
        else:
            matches[match.group(0)] = [match.start()]

pickle.dump(matches, open(dir + ".idx", "wb"))
