from nltk.corpus import wordnet
from nltk.corpus import semcor
from semcor_chunk import semcor_chunk
import argparse
import random

def parse_command_line():
	parser = argparse.ArgumentParser(description='Replace sentence \
		in the SemCor corpus at that index with a random synonym, \
		hypernym, or hyponym.')
	
	parser.add_argument('index', help='replace index', type=int)
	parser.add_argument('-nym', help='replace with synonym, hypernym, \
		or hyponym', type=str, choices=['synonym', 'hypernym', 'hyponym'])
	
	args = parser.parse_args()

	if not args.nym:
		parser.error('the following option is required: -nym')

	return args

def print_synonym_sentence(s):
	new_sentence = []
	for chunk in s:
		temp = semcor_chunk(chunk)
		synset = temp.get_syn_set()
		word = temp.get_words()
		if not synset:
			for w in word:
				new_sentence.append(w)
		else:
			l_synos = []
			for synonym in synset.lemma_names():
				if synonym not in l_synos:
					l_synos.append(synonym)
			if l_synos:
				random_index = random.randint(0, len(l_synos) - 1)
				new_sentence.append(l_synos[random_index])
			else:
				for w in word:
					new_sentence.append(w)
	print (' '.join(new_sentence))

def print_hypernym_sentence(s):
	new_sentence = []
	for chunk in s:
		temp = semcor_chunk(chunk)
		synset = temp.get_syn_set()
		word = temp.get_words()
		if not synset:
			for w in word:
				new_sentence.append(w)
		else:
			l_hypers = []
			for hyper_synset in synset.hypernyms():
				word = hyper_synset.name().split('.')[0]
				if word not in l_hypers:
					l_hypers.append(word)
			if l_hypers:
				random_index = random.randint(0, len(l_hypers) - 1)
				new_sentence.append(l_hypers[random_index])
			else:
				for w in word:
					new_sentence.append(w)
	print (' '.join(new_sentence))

def print_hyponym_sentence(s):
	new_sentence = []
	for chunk in s:
		temp = semcor_chunk(chunk)
		synset = temp.get_syn_set()
		word = temp.get_words()
		if not synset:
			for w in word:
				new_sentence.append(w)
		else:
			l_hypos = []
			for hypo_synset in synset.hyponyms():
				word = hypo_synset.name().split('.')[0]
				if word not in l_hypos:
					l_hypos.append(word)
			if l_hypos:
				random_index = random.randint(0, len(l_hypos) - 1)
				new_sentence.append(l_hypos[random_index])
			else:
				for w in word:
					new_sentence.append(w)
	print (' '.join(new_sentence))

if __name__ == "__main__":

	args = parse_command_line()

	l_sentence = semcor.sents()[args.index]
	sentence = ' '.join(l_sentence)

	print (sentence)

	s = semcor.tagged_sents(tag='sem')[args.index]
	# random.seed(a=0)

	if args.nym == 'synonym':
		print_synonym_sentence(s)
	elif args.nym == 'hypernym':
		print_hypernym_sentence(s)
	elif args.nym == 'hyponym':
		print_hyponym_sentence(s)