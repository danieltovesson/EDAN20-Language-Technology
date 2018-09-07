from sys import argv
import os
import re
import pickle

def getFiles(dir, suffix):
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
fileNames = getFiles(dir, ".txt")
matches = {}

def computeTF(wordDict):
    tfDict = {}
    bowCount = sum(wordDict.values())
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def computeIDF(wordPositions, fileNames):
    import math
    idfDict = {}
    N = len(fileNames)

    for word, val in wordPositions.items():
        idfDict[word] = math.log10(N / float(len(val)))

    return idfDict

def computeTFIDF(tf, idf):
    tfidf = {}
    for word, val in tf.items():
        tfidf[word] = val*idf[word]
    return tfidf

fileWordDict = {}
for fileName in fileNames:
    fileObject  = open(dir + "/" + fileName).read()
    fileWordDict[fileName] = {}
    for match in re.finditer(r"\w+", fileObject.lower()):
        if match.group(0) in matches:
            if fileName in matches[match.group(0)]:
                matches[match.group(0)][fileName].append(match.start())
            else:
                matches[match.group(0)][fileName] = [match.start()]
        else:
            matches[match.group(0)] = {fileName: [match.start()]}
        if match.group(0) not in fileWordDict[fileName]:
            fileWordDict[fileName][match.group(0)] = 0
        fileWordDict[fileName][match.group(0)] += 1

pickle.dump(matches, open(dir + ".idx", "wb"))

idf = computeIDF(matches, fileNames)
for fileName in fileNames:
    tf = computeTF(fileWordDict[fileName])
    tfidf = computeTFIDF(tf, idf)
    print(tfidf)
