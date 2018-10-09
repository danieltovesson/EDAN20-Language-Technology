"""
Gold standard parser
"""
__author__ = "Pierre Nugues"

import transition
import conll
import features

import conll_reader
from sklearn.feature_extraction import DictVectorizer
#from sklearn import svm
from sklearn import linear_model
#from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.externals import joblib

def reference(stack, queue, graph):
    """
    Gold standard parsing
    Produces a sequence of transitions from a manually-annotated corpus:
    sh, re, ra.deprel, la.deprel
    :param stack: The stack
    :param queue: The input list
    :param graph: The set of relations already parsed
    :return: the transition and the grammatical function (deprel) in the
    form of transition.deprel
    """
    # Right arc
    if stack and stack[0]['id'] == queue[0]['head']:
        # print('ra', queue[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + queue[0]['deprel']
        stack, queue, graph = transition.right_arc(stack, queue, graph)
        return stack, queue, graph, 'ra' + deprel
    # Left arc
    if stack and queue[0]['id'] == stack[0]['head']:
        # print('la', stack[0]['deprel'], stack[0]['cpostag'], queue[0]['cpostag'])
        deprel = '.' + stack[0]['deprel']
        stack, queue, graph = transition.left_arc(stack, queue, graph)
        return stack, queue, graph, 'la' + deprel
    # Reduce
    if stack and transition.can_reduce(stack, graph):
        for word in stack:
            if (word['id'] == queue[0]['head'] or
                        word['head'] == queue[0]['id']):
                # print('re', stack[0]['cpostag'], queue[0]['cpostag'])
                stack, queue, graph = transition.reduce(stack, queue, graph)
                return stack, queue, graph, 're'
    # Shift
    # print('sh', [], queue[0]['cpostag'])
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'

def parse_ml(stack, queue, graph, trans):
    trans = trans[0]
    if stack and trans[:2] == 'ra':
        stack, queue, graph = transition.right_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'ra'
    if stack and trans[:2] == 'la' and transition.can_leftarc(stack, graph):
        stack, queue, graph = transition.left_arc(stack, queue, graph, trans[3:])
        return stack, queue, graph, 'la'
    if stack and trans[:2] == 're' and transition.can_reduce(stack, graph):
        stack, queue, graph = transition.reduce(stack, queue, graph)
        return stack, queue, graph, 're'
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'

if __name__ == '__main__':
    train_file = 'datasets/swedish_talbanken05_train.conll'
    test_file = 'datasets/swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']
    feature_names_1 = ['stack0_word', 'stack0_POS', 'queue0_word', 'queue0_POS', 'can-la', 'can-re']
    feature_names_2 = ['stack0_word', 'stack0_POS', 'queue0_word', 'queue0_POS', 'can-la', 'can-re', 'stack1_word', 'stack1_POS', 'queue1_word', 'queue1_POS']
    feature_names_3 = ['stack0_word', 'stack0_POS', 'queue0_word', 'queue0_POS', 'can-la', 'can-re', 'stack1_word', 'stack1_POS', 'queue1_word', 'queue1_POS', 'stack_word_following_word', 'stack_following_POS', 'queue_following_word', 'queue_following_POS']
    feature_names = feature_names_1
    model_name_1 = 'model1'
    model_name_2 = 'model2'
    model_name_3 = 'model3'
    model_name = model_name_1
    out_file_name_1 = 'out1'
    out_file_name_2 = 'out2'
    out_file_name_3 = 'out3'
    out_file_name = out_file_name_1

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)

    print("Extracting the features...")
    sent_cnt = 0
    X = []
    y = []
    for sentence in formatted_corpus:
        sent_cnt += 1
        #if sent_cnt % 1000 == 0:
            #print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []
        while queue:
            X.append(features.extract(stack, queue, graph, feature_names, sentence))
            stack, queue, graph, trans = reference(stack, queue, graph)
            transitions.append(trans)
            y.append(trans)
        stack, graph = transition.empty_stack(stack, graph)
        #print('Equal graphs:', transition.equal_graphs(sentence, graph))

        # Poorman's projectivization to have well-formed graphs.
        for word in sentence:
            word['head'] = graph['heads'][word['id']]
        #print(transitions)
        #print(graph)

    vec = DictVectorizer(sparse=True)

    modelFilename = model_name + '.sav'
    try:
        classifier = joblib.load(modelFilename)
        vec.fit_transform(X)
        print("Model found in memory")
    except:
        print("Encoding the features...")
        X_fit_transform = vec.fit_transform(X)

        print("Training the model...")
        classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear')
        model = classifier.fit(X_fit_transform, y)
        print(model)

        joblib.dump(model, modelFilename)

        X_transform = vec.transform(X)
        y_predicted = classifier.predict(X_transform)
        print("Classification report for classifier %s:\n%s\n"
              % (classifier, metrics.classification_report(y, y_predicted)))

    keys = ['stack0_POS', 'stack1_POS', 'stack0_word', 'stack1_word', 'queue0_POS', 'queue1_POS', 'queue0_word', 'queue1_word', 'can-re', 'can-la', 'stack_following_POS', 'stack_word_following_word', 'queue_following_POS', 'queue_following_word']
    for i in range(9):
        x = []
        for key in keys:
            if key in X[i]:
                x.append(X[i][key])
        #print("x = ", end='')
        #print(x)
        #print("y = " + y[i])

    sentences = conll.read_sentences(test_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006_test)

    f_out = open(out_file_name, 'w', newline='\n')
    for sentence in formatted_corpus:
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []
        while queue:
            X_features = features.extract(stack, queue, graph, feature_names, sentence)
            X_transform = vec.transform(X_features)
            trans_pred = classifier.predict(X_transform)
            stack, queue, graph, trans = parse_ml(stack, queue, graph, trans_pred)
        stack, graph = transition.empty_stack(stack, graph)

        for word in sentence:
            word['head'] = graph['heads'][word['id']]
            word['deprel'] = graph['deprels'][word['id']]
            if int(word['id']) != 0:
                f_out.write(word['id'] + '\t' + word['form'] + '\t' + word['lemma'] + '\t' + word['cpostag'] + '\t' + word['postag'] + '\t' + word['feats'] + '\t' + word['head'] + '\t' + word['deprel'] + '\t_\t_')
                f_out.write('\n')
        f_out.write('\n')
