#!/usr/bin/env python3
"""
ANLP A4: Perceptron

Usage: python perceptron.py NITERATIONS

(Adapted from Alan Ritter)
"""
import sys, os, glob

from collections import Counter
from math import log
from numpy import mean
import numpy as np

from nltk.stem.wordnet import WordNetLemmatizer

from evaluation import Eval

def load_docs(direc, lemmatize, labelMapFile='labels.csv'):
	"""Return a list of word-token-lists, one per document.
	Words are optionally lemmatized with WordNet."""

	labelMap = {}   # docID => gold label, loaded from mapping file
	with open(os.path.join(direc, labelMapFile)) as inF:
		for ln in inF:
			docid, label = ln.strip().split(',')
			assert docid not in labelMap
			labelMap[docid] = label

	# create parallel lists of documents and labels
	docs, labels = [], []
	for file_path in glob.glob(os.path.join(direc, '*.txt')):
		filename = os.path.basename(file_path)
		# open the file at file_path, construct a list of its word tokens,
		# and append that list to 'docs'.
		# look up the document's label and append it to 'labels'.
		f = open(file_path, 'r')
		
		word_tokens = []

		# unigram
		word_tokens += f.read().strip().split()

		# bigram
		for line in f:
			words = line.split()
			if words:
				previous_word = '<s>'
				for w in words:
					word_tokens.append(previous_word + ' ' + w)
					previous_word = w

		# trigram
		for line in f:
			words = line.split()
			if words:
				pp_word = '<s>'
				p_word = '<s>'
				for w in words:
					word_tokens.append(pp_word + ' ' + p_word + ' ' + w)
					pp_word = p_word
					p_word = w

		# character unigram
		# word_tokens += list(f.read().replace(' ', '').replace('\n', ''))
		
		# character bigram
		# for line in f:
		# 	words = line.split()
		# 	if words:
		# 		for w in words:
		# 			p_char = '<s>'
		# 			for c in w:
		# 				word_tokens.append(p_char+c)
		# 				p_char = c

		# lowercase normalization
		# word_tokens = [w.lower() for w in word_tokens]

		# word length useless
		# temp = f.read().strip().split()
		# word_tokens += [len(t) for t in temp]
		
		# sentence length useless
		# for line in f:
		# 	words = line.split()
		# 	if words:
		# 		word_tokens.append(len(words))

		# debug
		# print (word_tokens)

		docs.append(word_tokens)
		labels.append(labelMap[filename])
		f.close()

	return docs, labels

def extract_feats(doc):
	"""
	Extract input features (percepts) for a given document.
	Each percept is a pairing of a name and a boolean, integer, or float value.
	A document's percepts are the same regardless of the label considered.
	"""
	ff = Counter(doc).most_common(100)
	li = []
	for i in ff:
		for j in range(i[1]):
			li.append(i[0])
	ff = Counter(li)
	return ff

def load_featurized_docs(datasplit):
	rawdocs, labels = load_docs(datasplit, lemmatize=False)
	assert len(rawdocs)==len(labels)>0,datasplit
	featdocs = []
	for d in rawdocs:
		featdocs.append(extract_feats(d))
	return featdocs, labels

class Perceptron:
	def __init__(self, train_docs, train_labels, MAX_ITERATIONS=100, dev_docs=None, dev_labels=None):
		self.CLASSES = ['ARA', 'DEU', 'FRA', 'HIN', 'ITA', 'JPN', 'KOR', 'SPA', 'TEL', 'TUR', 'ZHO']
		self.MAX_ITERATIONS = MAX_ITERATIONS
		self.dev_docs = dev_docs
		self.dev_labels = dev_labels
		self.weights = {l: Counter() for l in self.CLASSES}
		self.learn(train_docs, train_labels)

	def copy_weights(self):
		"""
		Returns a copy of self.weights.
		"""
		return {l: Counter(c) for l,c in self.weights.items()}

	def learn(self, train_docs, train_labels):
		"""
		Train on the provided data with the perceptron algorithm.
		Up to self.MAX_ITERATIONS of learning.
		At the end of training, self.weights should contain the final model
		parameters.
		"""
		for i in range(self.MAX_ITERATIONS):
			for j in range(len(train_docs)):
				if self.predict(train_docs[j]) != train_labels[j]:
					for word in train_docs[j]:
						self.weights[train_labels[j]][word] += 1 # change value to 2 if doing subtract all
						# subtract all others is too slow to implement
						# for k in range(len(self.CLASSES)):
						# 	self.weights[train_labels[k]][word] -= 1
					self.weights[train_labels[j]]['g_bias'] += 1 # change value to 2 if doing subtract all
					# subtract all others is too slow to implement
					# for k in range(len(self.CLASSES)):
					# 	self.weights[train_labels[k]]['g_bias'] -= 1
			# uncomment below lines for iteration analysis
			# print (str(i), str(self.test_eval(train_docs, train_labels)),
			# 	str(self.test_eval(self.dev_docs, self.dev_labels)), sep=',')
			print ('iter'+str(i), file=sys.stderr)

	def score(self, doc, label):
		"""
		Returns the current model's score of labeling the given document
		with the given label.
		"""
		score = 0
		for element in doc:
			score += doc[element] * self.weights[label][element]
		score += self.weights[label]['g_bias']
		return score

	def predict(self, doc):
		"""
		Return the highest-scoring label for the document under the current model.
		"""
		max_score = self.score(doc, self.CLASSES[0])
		predict_label = self.CLASSES[0]
		for i in range(1, len(self.CLASSES)):
			score = self.score(doc, self.CLASSES[i])
			if max_score <= score:
				max_score = score
				predict_label = self.CLASSES[i]
		return predict_label

	def test_eval(self, test_docs, test_labels):
		pred_labels = [self.predict(d) for d in test_docs]
		ev = Eval(test_labels, pred_labels)
		# ev.print_mx() # print confusion mx
		return ev.accuracy()

	def print_10_highest_lowest(self):
		for i in self.CLASSES:
			print(i)
			most_common = self.weights[i].most_common(10)
			least_common = self.weights[i].most_common()[:-11:-1]
			print('10 highest-weighted features', end=',')
			print (','.join([str(j[0]) for j in most_common]))
			print('weights', end=',')
			print (','.join([str(j[1]) for j in most_common]))
			print('10 lowest-weighted features', end=',')
			print (','.join([str(j[0]) for j in least_common]))
			print('weights', end=',')
			print (','.join([str(j[1]) for j in least_common]))
			print('bias,'+str(self.weights[i]['g_bias']))

if __name__ == "__main__":
	args = sys.argv[1:]
	niters = int(args[0])

	train_docs, train_labels = load_featurized_docs('train')
	print(len(train_docs), 'training docs with',
		sum(len(d) for d in train_docs)/len(train_docs), 'percepts on avg', file=sys.stderr)

	dev_docs,  dev_labels  = load_featurized_docs('dev')
	print(len(dev_docs), 'dev docs with',
		sum(len(d) for d in dev_docs)/len(dev_docs), 'percepts on avg', file=sys.stderr)


	test_docs,  test_labels  = load_featurized_docs('test')
	print(len(test_docs), 'test docs with',
		sum(len(d) for d in test_docs)/len(test_docs), 'percepts on avg', file=sys.stderr)

	# print('iteration', 'trainAcc', 'devAcc', sep=',') # uncomment this line of header for not generating confusion mx
	ptron = Perceptron(train_docs, train_labels, MAX_ITERATIONS=niters, dev_docs=dev_docs, dev_labels=dev_labels)
	ptron.print_10_highest_lowest() # print 10 highest and 10 lowest weights features
	acc = ptron.test_eval(test_docs, test_labels)
	print(acc, file=sys.stderr)
