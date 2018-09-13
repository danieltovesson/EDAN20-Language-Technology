

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
    cw = []
    numberOfWords = []
    pw = []

    for token in tokensSentence:
        if token in unigramCounts:
            cw.append(unigramCounts[token])
        else:
            cw.append(0)
    for cwi in cw: numberOfWords.append(len(tokensText))
    for cwi in cw: pw.append(cwi/numberOfWords[0])

    unigramModel.append(tokensSentence)
    unigramModel.append(cw)
    unigramModel.append(numberOfWords)
    unigramModel.append(pw)

    return unigramModel

def buildBigramModel(tokensText, tokensSentence):
    from mutual_info import count_unigrams

    bigramModel = []

    bigramCounts = count_unigrams(tokensText)
    cw = []
    numberOfWords = []
    pw = []

    for token in tokensSentence:
        if token in bigramCounts:
            cw.append(bigramCounts[token])
        else:
            cw.append(0)
    for cwi in cw: numberOfWords.append(len(tokensText))
    for cwi in cw: pw.append(cwi/numberOfWords[0])

    bigramModel.append(tokensSentence)
    bigramModel.append(cw)
    bigramModel.append(numberOfWords)
    bigramModel.append(pw)

    return bigramModel

def printModel(model):
    import numpy as np
    model = np.flipud(np.rot90(model))
    for i in model:
        row = ''
        for j in i:
            row += j + '\t'
        print(row)

(tokensText, tokensSentence) = generateTokens()

print('Unigram model')
print('=====================================================')
print('wi\tC(wi)\t#words\tP(wi)')
print('=====================================================')

unigramModel = buildUnigramModel(tokensText, tokensSentence)
printModel(unigramModel)

print('Bigram model')
print('=====================================================')
print('wi\twi+1\tCi,i+1\tC(i)\tP(wi+1|wi)')
print('=====================================================')

bigramModel = buildBigramModel(tokensText, tokensSentence)
printModel(bigramModel)
