import sys
import re
import os

import sentencepiece as spm

def load_corpus(file_directory):
	corpus = []

	f = open(file_directory, 'r')
	raw = f.read()
	data = raw.splitlines()
	raw = re.sub('[^" ""\n"\u0E00-\u0E7F]+', '', raw)
	f.close()

	for line in data[1:]:
		comment = ''.join(x for x in line.split(':')[2:])
		corpus.append(comment)

	return corpus, raw

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

	corpus, raw = load_corpus('../data/' + file_name)
	print('Total documents', len(corpus))

	f = open('train_' + file_name, 'w')
	f.write(raw)
	f.close()

	spm.SentencePieceTrainer.Train('--input=train_' + file_name + ' --model_prefix=m --vocab_size=1000')
	tokenizer = spm.SentencePieceProcessor()
	tokenizer.Load('m.model')

	with open('../data/tokenized/sentencepiece/tokenized_' + file_name, 'w') as f:
		f.write('[')
		for doc in corpus:
			cleaned_doc = clean(doc)
			print(cleaned_doc)
			tokenized_doc = tokenizer.EncodeAsPieces(cleaned_doc)
			f.write('[')
			for word in tokenized_doc:
				word = re.sub('▁', '', word)
				if word != ' ' and word != '':
					f.write('\'' + word + '\',')
			f.write('],')
		f.write(']')

	os.remove('train_' + file_name)
	os.remove('m.model')
	os.remove('m.vocab')

if __name__ == "__main__":
  main()
