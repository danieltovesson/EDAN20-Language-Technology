import transition

def extract(stack, queue, graph, feature_names, sentence):
    features = []

    # Feature set 1
    features.extend([None, None, None, None, None, None])
    if len(stack) >= 1:
        features[0] = stack[0]['form']
        features[1] = stack[0]['postag']
    if len(queue) >= 1:
        features[2] = queue[0]['form']
        features[3] = queue[0]['postag']
    features[4] = transition.can_leftarc(stack, graph)
    features[5] = transition.can_reduce(stack, graph)

    # Feature set 2
    if len(feature_names) == 10 or len(feature_names) == 14:
        features.extend([None, None, None, None])
        if len(stack) >= 2:
            features[6] = stack[1]['form']
            features[7] = stack[1]['postag']
        if len(queue) >= 2:
            features[8] = queue[1]['form']
            features[9] = queue[1]['postag']

    # Feature set 3
    if len(feature_names) == 14:
        features.extend([None, None, None, None])
        if len(stack) >= 1 and len(sentence) > int(stack[0]['id']) + 1:
            word = sentence[int(stack[0]['id']) + 1]
            features[10] = word['form']
            features[11] = word['postag']
        if len(queue) >= 1 and len(sentence) > int(queue[0]['id']) + 1:
            word = sentence[int(queue[0]['id']) + 1]
            features[12] = word['form']
            features[13] = word['postag']

    return features
