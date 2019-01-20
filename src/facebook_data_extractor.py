from bs4 import BeautifulSoup
from bs4.element import NavigableString

import re
import sys

def main():
	file_name = sys.argv[1]
	if not file_name:
		return

	with open(file_name) as html:
		soup = BeautifulSoup(html, 'html.parser')

	comment_container = soup.find('div', {'class': 'permalinkPost'})
	comment_container = comment_container.find('div', {'class': 'UFIList'})
	comments = comment_container.find_all('div', {'class': 'UFICommentActorAndBodySpacing'})

	skip = 0
	file_name = file_name.replace('html', 'txt')
	with open('../data/facebook/' + file_name, 'w') as f:
		f.write('comment::\n')
		row = 0
		for comment in comments:
		    if comment.find('a', {'class': 'profileLink'}):
		        skip += 1
		        continue

		    comment = comment.find('span', {'class': 'UFICommentBody'})
		    comment_children = comment.descendants
		    comment = ''
		    for child in comment_children:
		    	if isinstance(child, NavigableString):
		    		comment += child

		    comment = comment.strip()
		    if comment == '' or comment.isdigit():
		        continue
		    f.write('comment' + str(row) + '::' + comment + '\n')
		    row += 1
	print('Skip ' + str(skip) + ' comments.')
	
if __name__ == "__main__":
  main()
