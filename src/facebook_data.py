from bs4 import BeautifulSoup

import os
import re

def clean(doc):
    while True:
        new_doc = re.sub('[^\u0E00-\u0E7F]+', '', doc)
        if doc == new_doc:
            break
        else:
            doc = new_doc

    return doc

with open('../data/facebook/2/ผู้บริโภค - VillaMarket.html') as html:
    soup = BeautifulSoup(html, 'html.parser')

comment_container = soup.find('div', {'class': 'fbPhotosSnowliftFeedback'})
comment_container = comment_container.find('div', {'class': 'UFIList'})
comments = comment_container.find_all('div', {'class': 'UFICommentActorAndBodySpacing'})

file_name = '../data/facebook/ผู้บริโภค - VillaMarket.txt'
os.makedirs(os.path.dirname(file_name), exist_ok=True)

with open(file_name, 'w') as f:
    f.write('comment::\n')

    for i, comment in enumerate(comments):
        comment = comment.find('span', {'class': 'UFICommentBody'})
        comment = clean(str(comment))
        if comment == '':
            continue
        f.write('comment' + str(i) + '::' + comment + '\n')
