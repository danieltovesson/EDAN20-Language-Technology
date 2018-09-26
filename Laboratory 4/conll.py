"""
CoNLL-X and CoNLL-U file readers and writers
"""
__author__ = "Pierre Nugues"

import os


def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    Recursive version
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        path = dir + '/' + file
        if os.path.isdir(path):
            files += get_files(path, suffix)
        elif os.path.isfile(path) and file.endswith(suffix):
            files.append(path)
    return files


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    f = open(file).read().strip()
    sentences = f.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    root_values = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
    start = [dict(zip(column_names, root_values))]
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split())) for row in rows if row[0] != '#']
        sentence = start + sentence
        new_sentences.append(sentence)
    return new_sentences

def extract_subject_verb_pairs(formatted_corpus):
    import operator
    subject_verb_pairs = {}
    tot_num_pairs = 0
    for sentence in formatted_corpus:
        for word in sentence:
            if (word['deprel'] == 'SS'):
                head = sentence[int(word['head'])]
                subject = str.lower(word['form'])
                verb =  str.lower(head['form'])
                chunk = (subject, verb)
                tot_num_pairs += 1
                if chunk in subject_verb_pairs:
                    subject_verb_pairs[chunk] += 1
                else:
                    subject_verb_pairs[chunk] = 1
    subject_verb_pairs = sorted(subject_verb_pairs.items(), key=operator.itemgetter(1))
    return (subject_verb_pairs, tot_num_pairs)

def extract_subject_verb_object_triples(formatted_corpus):
    import operator
    subject_verb_object_triples = {}
    tot_num_triples = 0
    for sentence in formatted_corpus:
        subjects = []
        objects = []
        for word in sentence:
            if (word['deprel'] == 'SS'):
                subjects.append(word)
            if (word['deprel'] == 'OO'):
                objects.append(word)
        for s in subjects:
            for o in objects:
                if s['head'] == o['head']:
                    head = sentence[int(s['head'])]
                    subject = str.lower(s['form'])
                    verb = str.lower(head['form'])
                    object = str.lower(o['form'])
                    chunk = (subject, verb, object)
                    tot_num_triples += 1
                    if chunk in subject_verb_object_triples:
                        subject_verb_object_triples[chunk] += 1
                    else:
                        subject_verb_object_triples[chunk] = 1
    subject_verb_object_triples = sorted(subject_verb_object_triples.items(), key=operator.itemgetter(1))
    return (subject_verb_object_triples, tot_num_triples)

def save(file, formatted_corpus, column_names):
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence[1:]:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()


if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    train_file = 'datasets/swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'datasets/swedish_talbanken05_test.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    #print(train_file, len(formatted_corpus))
    #print(formatted_corpus)

    (subject_verb_pairs, tot_num_pairs) = extract_subject_verb_pairs(formatted_corpus)

    (subject_verb_object_triples, tot_num_triples) = extract_subject_verb_object_triples(formatted_corpus)

    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

    files = get_files('../../corpus/ud-treebanks-v1.3/', 'train.conllu')
    for train_file in files:
        sentences = read_sentences(train_file)
        formatted_corpus = split_rows(sentences, column_names_u)
        print(train_file, len(formatted_corpus))
        print(formatted_corpus[0])
