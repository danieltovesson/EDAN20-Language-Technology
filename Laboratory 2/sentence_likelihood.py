def generateTokens():
    import sys
    from mutual_info import tokenize

    text = sys.stdin.read().lower()
    sentence = sys.argv[1].lower()

    tokensText = tokenize(text)
    tokensSentence = tokenize(sentence)

    return tokensText, tokensSentence

def buildUnigramModel(tokensText, tokensSentence):
    from mutual_info import count_unigrams

    unigramModel = []
    unigramCounts = count_unigrams(tokensText)

    unigramModel.append(tokensSentence)

    wordCounts = []
    for token in tokensSentence:
        if token in unigramCounts:
            wordCounts.append(unigramCounts[token])
        else:
            wordCounts.append(0)
    unigramModel.append(wordCounts)

    totalNumberOfWords = []
    for word in tokensSentence: totalNumberOfWords.append(len(tokensText))
    unigramModel.append(totalNumberOfWords)

    wordProbability = []
    for wordCount in wordCounts: wordProbability.append(wordCount/len(tokensText))
    unigramModel.append(wordProbability)

    unigramModel = flipMatrix(unigramModel)

    return unigramModel, wordProbability

def buildBigramModel(tokensText, tokensSentence):
    from mutual_info import count_unigrams, count_bigrams

    bigramModel = []
    unigramCountsText = count_unigrams(tokensText)
    bigramCountsSentence = count_bigrams(tokensSentence)
    bigramCountsText = count_bigrams(tokensText)

    words1 = []
    words2 = []
    for bigram in bigramCountsSentence.keys():
        words1.append(bigram[0])
        words2.append(bigram[1])
    bigramModel.append(words1)
    bigramModel.append(words2)

    bigramCounts = []
    for bigram in bigramCountsSentence:
        if bigram in bigramCountsText:
            bigramCounts.append(bigramCountsText[bigram])
        else:
            bigramCounts.append(0)
    bigramModel.append(bigramCounts)

    word1Counts = []
    for bigram in bigramCountsSentence:
        word1 = bigram[0]
        if word1 in unigramCountsText:
            word1Counts.append(unigramCountsText[word1])
        else:
            word1Counts.append(0)
    bigramModel.append(word1Counts)

    bigramProbability = []
    for i in range(len(bigramCounts)):
        if bigramCounts[i] != 0:
            bigramProbability.append(bigramCounts[i]/word1Counts[i])
        else:
            bigramProbability.append(0)
            if words1[i] in unigramCountsText:
                bigramProbability.append('*backoff: ' + str(unigramCountsText[words2[i]]/len(tokensText)))
    bigramModel.append(bigramProbability)

    bigramModel = flipMatrix(bigramModel)

    return bigramModel, bigramProbability

def flipMatrix(matrix):
    flippedMatrix = []
    for i in range(len(matrix[0])): flippedMatrix.append([])
    for row in matrix:
        for index, value in enumerate(row):
            if index < len(flippedMatrix):
                flippedMatrix[index].append(value)
            else:
                flippedMatrix[index-1].append(value) # Special case for backoff
    return flippedMatrix

def calculateProbUnigrams(wordProbability):
    import numpy as np
    wordProbability = cleanWordProbabilityArray(wordProbability)
    probUnigrams = np.prod(wordProbability)
    return ['Prob. unigrams:', probUnigrams]

def calculateProbBigrams(bigramProbability):
    import numpy as np
    bigramProbability = cleanBigramProbabilityArray(bigramProbability)
    probBigrams = np.prod(bigramProbability)
    return ['Prob. bigrams:', probBigrams]

def calculateGeoMeanUnigram(wordProbability):
    import numpy as np
    import math
    wordProbability = cleanWordProbabilityArray(wordProbability)
    geoMeanProb = np.prod(wordProbability)
    geoMeanProb = math.pow(geoMeanProb, 1/len(wordProbability))
    return ['Geometric mean prob.:', geoMeanProb]

def calculateGeoMeanBigram(wordProbability, bigramProbability):
    import numpy as np
    import math
    bigramProbability.pop(0)
    bigramProbability = cleanBigramProbabilityArray(bigramProbability)
    geoMeanProb = np.prod(bigramProbability)
    geoMeanProb *= wordProbability[0]
    geoMeanProb = math.pow(geoMeanProb, 1/len(bigramProbability))
    return ['Geometric mean prob.:', geoMeanProb]

def calculateEntropyRate():
    return ['Entropy rate:', 0]

def calculatePerplexity():
    return ['Perplexity:', 0]

def cleanWordProbabilityArray(wordProbability):
    return [x for x in wordProbability if not x == 0]

def cleanBigramProbabilityArray(bigramProbability):
    return [x for x in bigramProbability if not isinstance(x, str) and not x == 0]

def printModel(model):
    import numpy as np
    for i in model:
        row = ''
        for j in i:
            row += str(j) + '\t'
        print(row)

tokensText, tokensSentence = generateTokens()

print('Unigram model')
print('=====================================================')
print('wi\tC(wi)\t#words\tP(wi)')
print('=====================================================')

unigramModel, wordProbability = buildUnigramModel(tokensText, tokensSentence)
printModel(unigramModel)

print('=====================================================')

results = []
results.append(calculateProbUnigrams(wordProbability))
results.append(calculateGeoMeanUnigram(wordProbability))
results.append(calculateEntropyRate())
results.append(calculatePerplexity())
printModel(results)

print('\n')

print('Bigram model')
print('=====================================================')
print('wi\twi+1\tCi,i+1\tC(i)\tP(wi+1|wi)')
print('=====================================================')

bigramModel, bigramProbability = buildBigramModel(tokensText, tokensSentence)
printModel(bigramModel)

print('=====================================================')

results = []
results.append(calculateProbBigrams(bigramProbability))
results.append(calculateGeoMeanBigram(wordProbability, bigramProbability))
results.append(calculateEntropyRate())
results.append(calculatePerplexity())
printModel(results)

print('\n')
