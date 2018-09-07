from sys import argv
import os
import re
import pickle
from scipy import spatial

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
tfidfs = {}
for fileName in fileNames:
    tf = computeTF(fileWordDict[fileName])
    tfidf = computeTFIDF(tf, idf)
    tfidfs[fileName] = tfidf

cosineSimilarityMatrix = []

cosineSimilarityMatrix.append([""] + fileNames)
for file, tfidf in tfidfs.items():
    row = [file]
    for fileName in fileNames:
        dataSetI = []
        dataSetII = []
        for word, val in tfidf.items():
            dataSetI.append(val)
            dataSetII.append(tfidfs[fileName][word] if word in tfidfs[fileName] else 0)
        result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
        row.append(round(result, 8))
    cosineSimilarityMatrix.append(row)

s = [[str(e) for e in row] for row in cosineSimilarityMatrix]
lens = [max(map(len, col)) for col in zip(*s)]
fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
table = [fmt.format(*row) for row in s]
print('\n'.join(table))
