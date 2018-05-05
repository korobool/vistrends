import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.tree import Tree

stopwords = stopwords.words('english')


def get_noun_phrases(text):
    if len(text) < 5:
        return []
    result = []
    # text = """The Buddha, the Godhead, resides quite as comfortably in the circuits of a digital \
    # computer or the gears of a cycle transmission as he does at the top of a mountain \
    # or in the petals of a flower. To think otherwise is to demean the Buddha...which is \
    # to demean oneself."""
    # print(text)

    sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
    lemmatizer = nltk.WordNetLemmatizer()
    stemmer = nltk.stem.porter.PorterStemmer()

    # Taken from Su Nam Kim Paper...
    grammar = r"""
        NBAR:
            {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

        NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)
    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)
    # print(postoks)
    tree = chunker.parse(postoks)

    def leaves(tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            yield subtree.leaves()

    def normalise(word):
        """Normalises words to lowercase and stems and lemmatizes it."""
        word = word.lower()
        # word = stemmer.stem_word(word) #if we consider stemmer then results comes with stemmed word, but in this case word will not match with comment
        word = lemmatizer.lemmatize(word)
        return word

    def acceptable_word(word):
        """Checks conditions for acceptable word: length, stopword. We can increase the length if we want to consider
        large phrase """
        accepted = bool(2 <= len(word) <= 40
                        and word.lower() not in stopwords)
        return accepted

    def get_terms(tree):
        for leaf in leaves(tree):
            term = [normalise(w) for w, t in leaf if acceptable_word(w)]
            yield term

    terms = get_terms(tree)

    for term in terms:
        result.append(' '.join(term))
    return result


def get_ner_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    return continuous_chunk


def get_entities(text):
    result = []
    ne = get_ner_chunks(text)
    np = get_noun_phrases(text)
    # print(np)
    # print(ne)
    if np:
        result.extend(np)
    if ne:
        result.extend(ne)

    return result


def get_joined_entities(text):
    entities = get_entities(text)
    return [item.replace(' ', '_') for item in entities]


def ngram_chunk(text, bigram=True, trigram=False):
    result = []
    tokens = text.split()
    if bigram:
        for i, word in enumerate(tokens):
            if i < len(tokens) - 2:
                result.append('_'.join(tokens[i:i + 2]))
    if trigram:
        for i, word in enumerate(tokens):
            if i < len(tokens) - 3:
                result.append('_'.join(tokens[i:i + 3]))

    return ' '.join(result)


if __name__ == "__main__":
    print(get_entities(
        'If you want to learn how to play the PUBG test servers, like this tweet and I will message you the '
        'instructions. #PUBG @PUBG'))
