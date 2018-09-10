from sys import argv

# Premade method that was supported from assignment description.
def getFiles(dir, suffix):
    import os
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

# Calculate TF
def computeTF(wordDict):
    tfDict = {}
    bowCount = sum(wordDict.values())
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

# Calculate IDF
def computeIDF(wordPositions, fileNames):
    import math
    idfDict = {}
    N = len(fileNames)

    for word, val in wordPositions.items():
        idfDict[word] = math.log10(N / float(len(val)))

    return idfDict

# Combines and calculates TF-IDF values.
def computeTFIDF(tf, idf):
    tfidf = {}
    for word, val in tf.items():
        tfidf[word] = val*idf[word]
    return tfidf

# Creates a index file aswell as returning useful vectors in order to calculate TF-IDF values.
def indexMaker(dir):
    import re
    import pickle
    fileNames = getFiles(dir, ".txt")
    matches = {}
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
    return (fileNames, matches, fileWordDict)

# Computes TF and IDF values and returns them for cosine similary matrix.
def extractTFIDF(matches, fileNames):
    idf = computeIDF(matches, fileNames)
    tfidfs = {}
    for fileName in fileNames:
        tf = computeTF(fileWordDict[fileName])
        tfidf = computeTFIDF(tf, idf)
        tfidfs[fileName] = tfidf
    return tfidfs

# Calculates the cosineSimilarityMatrix, comparing the TF-IDF values.
def calcCosineSimilarityMatrix(tfidfs, fileNames):
    from scipy import spatial
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
    return cosineSimilarityMatrix

# Formats the cosineSimilarityMatrix so that it is readable.
def makeMatrixPretty(cosineSimilarityMatrix):
    s = [[str(e) for e in row] for row in cosineSimilarityMatrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

# Run program from terminal: ´python indexer.py selma´.
# Make sure that scipy is installed.
dir = argv[1]
(fileNames, matches, fileWordDict) = indexMaker(dir)
tfidfs = extractTFIDF(matches, fileNames)
cosineMatrix = calcCosineSimilarityMatrix(tfidfs, fileNames)
makeMatrixPretty(cosineMatrix)
