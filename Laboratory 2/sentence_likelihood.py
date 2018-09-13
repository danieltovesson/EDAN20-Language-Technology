def buildUnigramModel():
    import sys
    from mutual_info import tokenize, count_unigrams

    text = sys.stdin.read().lower()
    sentence = sys.argv[1].lower()

    unigramModel = []

    tokensText = tokenize(text)
    tokensSentence = tokenize(sentence)

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

print('Unigram model')
print('=====================================================')
print('wi C(wi) #words P(wi)')
print('=====================================================')
unigramModel = buildUnigramModel()

for unigram in unigramModel:
    print(unigram)
