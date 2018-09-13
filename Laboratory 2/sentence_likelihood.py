

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
    from mutual_info import count_bigrams, count_unigrams

    bigramModel = []

    bigramCountsSentence = count_bigrams(tokensSentence)
    bigramCountsText = count_bigrams(tokensText)
    unigramCountsText = count_unigrams(tokensText)

    wi = []
    wi1 = []
    cii1 = []
    ci = []
    pw = []

    for bigram in bigramCountsSentence.keys():
        wi.append(bigram[0])
        wi1.append(bigram[1])
    for bigram in bigramCountsSentence:
        if bigram in bigramCountsText:
            cii1.append(bigramCountsText[bigram])
            if bigram[0] in unigramCountsText:
                ci.append(unigramCountsText[bigram[0]])
            else:
                ci.append(0)
        else:
            if bigram[0] in unigramCountsText:
                ci.append(unigramCountsText[bigram[0]])
            else:
                ci.append(0)
            cii1.append(0)
    for idx, value in enumerate(cii1):
        if ci[idx] != 0:
         pw.append(value/ci[idx])
        else:
         pw.append(0)

    bigramModel.append(wi)
    bigramModel.append(wi1)
    bigramModel.append(cii1)
    bigramModel.append(ci)
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
