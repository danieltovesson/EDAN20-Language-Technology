"""
Sentences tokenizer
Usage: python tokenize_sentences.py < corpus.txt
"""
__author__ = "Daniel Tovesson & John Helbrink"

def findSentences(text):
    import regex as re
    text = re.sub('\s+', ' ', text, flags = re.MULTILINE)
    matches = re.findall('([\p{Lu}][^.]*[.])', text)
    result = ''
    for match in matches:
        result += '<s> ' + match + ' </s> '
    return result

def stripSentences(text):
    import regex as re
    text = re.sub('[\.,?!]+', ' ', text)
    text = text.lower()
    return text

#text = findSentences(text)
#text = stripSentences(text)
#print(text, end='')
