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

    return (unigramModel, pw)

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
            if value != 0:
                pw.append(value/ci[idx])
            else:
                if wi1[idx] in unigramCountsText:
                    pw.append('*backoff: ' + str(unigramCountsText[wi1[idx]]/len(tokensText)))
                else:
                    pw.append(0)
        else:
            if wi1[idx] in unigramCountsText:
                pw.append(unigramCountsText[wi1[idx]]/len(unigramCountsText))
            else:
                pw.append(0)

    bigramModel.append(wi)
    bigramModel.append(wi1)
    bigramModel.append(cii1)
    bigramModel.append(ci)
    bigramModel.append(pw)

    return (bigramModel, pw)

def calculateGeoMeanUnigram(pw):
    import math
    prob = 1
    for val in pw:
        prob *= val
    prob = math.pow(prob, 1/len(pw))
    return [['Geometric mean prob.:'], [prob]]

def calculateGeoMeanBigram(pwUni, pwBi):
    import math
    prob = 1
    pwBi[0] = pwUni[0]
    for val in pwUni:
        if isinstance(val, str):
            val = val.replace('*backoff: ', '')
        prob *= val
    prob = math.pow(prob, 1/len(pwBi))
    return [['Geometric mean prob.:'], [prob]]

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

(unigramModel, pwUni) = buildUnigramModel(tokensText, tokensSentence)
printModel(unigramModel)

print('=====================================================')

printModel(calculateGeoMeanUnigram(pwUni))

print('\n')

print('Bigram model')
print('=====================================================')
print('wi\twi+1\tCi,i+1\tC(i)\tP(wi+1|wi)')
print('=====================================================')

(bigramModel, pwBi) = buildBigramModel(tokensText, tokensSentence)
printModel(bigramModel)

print('=====================================================')

printModel(calculateGeoMeanBigram(pwUni, pwBi))

print('\n')
