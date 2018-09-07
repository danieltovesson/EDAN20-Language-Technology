from sys import argv
import re
import pickle

file_name = argv[1]
file_object  = open(file_name).read()

matches = {}
for match in re.finditer(r"\w+", file_object.lower()):
    if match.group(0) in matches:
        matches[match.group(0)].append(match.start())
    else:
        matches[match.group(0)] = [match.start()]

file_name = file_name.replace(".txt", "")
pickle.dump(matches, open(file_name + ".idx", "wb"))
