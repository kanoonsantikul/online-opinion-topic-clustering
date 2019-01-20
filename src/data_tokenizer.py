import sys
import re

from pythainlp.tokenize import word_tokenize

def load_corpus(file_directory):
	corpus = []
	labels = []

	f = open(file_directory, 'r')
	data = f.read().splitlines()
	f.close()

	start = False
	num = -2

	for line in data:
		if line.startswith('comment'):
			num += 1
			if num < 0:
				continue

			comment = ''.join(x for x in line.split(':')[2:])
			corpus.insert(num, comment)
			labels.insert(num, line.split(':')[1])
			start = True

		elif start:
			corpus[num] += line

	return corpus, labels

def clean(doc):
	while True:
		new_doc = re.sub('[^" "\u0E00-\u0E7F]+', '', doc)
		if doc == new_doc:
			break
		else:
			doc = new_doc
	doc = doc.strip()
	return doc

def main():
	file_name = sys.argv[1]
	if not file_name:
		return

	corpus = load_corpus('../data/facebook/' + file_name)[0]
	print('Total documents', len(corpus))

	with open('../data/facebook/tokenized/tokenized_' + file_name, 'w') as f:
		f.write('[')
		for doc in corpus:
			cleaned_doc = clean(doc)
			print(cleaned_doc)
			tokenized_doc = word_tokenize(cleaned_doc, engine='deepcut')
			f.write('[')
			for word in tokenized_doc:
				f.write('\'' + word + '\',')
			f.write('],')
		f.write(']')

if __name__ == "__main__":
  main()
