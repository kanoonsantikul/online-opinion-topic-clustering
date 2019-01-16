from bs4 import BeautifulSoup
from bs4.element import NavigableString

import os
import re

def clean(doc):
    while True:
        new_doc = re.sub('[^" "0-9\u0E00-\u0E7F]+', '', doc)
        if doc == new_doc:
            break
        else:
            doc = new_doc

    return doc.strip()

with open('จบข่าว - ใบขับขี่.html') as html:
    soup = BeautifulSoup(html, 'html.parser')

comment_container = soup.find('div', {'class': 'permalinkPost'})
comment_container = comment_container.find('div', {'class': 'UFIList'})
comments = comment_container.find_all('div', {'class': 'UFICommentActorAndBodySpacing'})

file_name = './new_file.txt'
os.makedirs(os.path.dirname(file_name), exist_ok=True)

skip = 0
with open(file_name, 'w') as f:
    f.write('comment::\n')

    for i, comment in enumerate(comments):
        if comment.find('a', {'class': 'profileLink'}):
            skip += 1
            continue

        comment = comment.find('span', {'class': 'UFICommentBody'})
        comment_children = comment.descendants
        comment = ''
        for child in comment_children:
        	if isinstance(child, NavigableString):
        		comment += child

        comment = clean(str(comment))
        if comment == '' or comment.isdigit():
            continue
        f.write('comment' + str(i) + '::' + comment + '\n')
print('Skip ' + str(skip) + ' comments.')
