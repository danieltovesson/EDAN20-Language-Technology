"""
Sentences tokenizer
Usage: python tokenize_sentences.py < corpus.txt
"""
__author__ = "Daniel Tovesson & John Helbrink"

def findSentences():
    import sys
    import regex as re
    text = sys.stdin.read()
    matches = re.findall('([\p{Lu}][^.]*[.])', text)
    result = ''
    for match in matches:
        result += '<s>' + match + '</s>\n'
    return result

print(findSentences(), end='')
