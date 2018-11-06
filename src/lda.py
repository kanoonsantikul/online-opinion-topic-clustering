import gensim
from gensim import corpora

from pythainlp.tokenize import word_tokenize

import re

def clean(doc):
    while True:
        new_doc = re.sub('[^\u0E00-\u0E7F]+', '', doc)
        if doc == new_doc:
            break
        else:
            doc = new_doc

    return doc

def remove_stop_words (corpus, dictionary, threshold):
    TfidfModel = gensim.models.TfidfModel
    tfidf = TfidfModel(corpus, dictionary)

    stop_words = []
    for doc in corpus:
        stop_words += [id for id, value in tfidf[doc] if value < threshold]

    dictionary.filter_tokens(bad_ids=stop_words)
    return dictionary

def get_tokenized_data(file_directory):
    comments = []

    with open(file_directory) as f:
        start = False
        num = -2

        for line in f:
            if line.startswith('comment'):
                num += 1
                if num < 0:
                    continue

                comment = ''.join(x for x in line.split(':')[2:])
                comments.insert(num, comment)
                start = True

            elif start:
                comments[num] += line

    for num in range(len(comments)):
        comments[num] = clean(comments[num])
        comments[num] = word_tokenize(comments[num], engine='newmm')

    return comments

comments = get_tokenized_data('../data/70-79/marked/31629130.txt')
print('Total documents ' + str(len(comments)))

dictionary = corpora.Dictionary(comments)
corpus = [dictionary.doc2bow(doc) for doc in comments]

dictionary = remove_stop_words(corpus, dictionary, 0.1)
corpus = [dictionary.doc2bow(doc) for doc in comments]

for i, doc in enumerate(corpus):
    print(str(i) + ': ', end='')
    for id, value in doc:
        print('(' + dictionary[id] + ', ' + str(value) + ')', end=' ')
    print('')

Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(corpus, num_topics=6, id2word=dictionary, passes=50)

print('\nterm-topic-matrix')
print(ldamodel.get_topics())

print('\ntopic term')
for i in range(6):
    print(ldamodel.show_topic(i, topn=10))
