import codecs
import numpy as np
from sklearn.preprocessing import normalize
from generate import GENERATE
import random

vocab = codecs.open("brown_vocab_100.txt", "r", encoding="utf-16")

#load the indices dictionary
word_index_dict = {}
for i, line in enumerate(vocab):
    #TODO: import part 1 code to build dictionary
    word_index_dict[line.rstrip()] = i

vocab.close()

f = codecs.open("brown_100.txt", 'r', encoding = "utf-16")

#TODO: initialize numpy 0s array
counts = np.zeros((len(word_index_dict), len(word_index_dict)), dtype=np.float)

#TODO: iterate through file and update counts
for line in f:
	words = line.split()
	previous_word = '<s>'
	for w in words:
		w = w.lower()
		if w in word_index_dict and previous_word in word_index_dict:
			counts[word_index_dict[previous_word]][word_index_dict[w]] += 1
		previous_word = w

f.close()

#TODO: normalize counts
counts += 0.1
probs = normalize(counts, norm='l1', axis=1)

#TODO: writeout bigram probabilities
output_file = open('smooth_probs.txt', 'w')
print(str(probs[word_index_dict['all']][word_index_dict['the']]), file=output_file)
print(str(probs[word_index_dict['the']][word_index_dict['jury']]), file=output_file)
print(str(probs[word_index_dict['the']][word_index_dict['campaign']]), file=output_file)
print(str(probs[word_index_dict['anonymous']][word_index_dict['calls']]), file=output_file)

output_file.close()

# below is the code for problem6
f = codecs.open("toy_corpus.txt", 'r', encoding = "utf-16")
output_file = open('smoothed_eval.txt', 'w')

for line in f:
	words = line.split()
	del words[0] # not sure if it is correct
	sentprob = 1
	previous_word = '<s>'
	for w in words:
		w = w.lower()
		sentprob *= probs[word_index_dict[previous_word]][word_index_dict[w]]
		previous_word = w
	# print(str(sentprob), file=output_file)

	sent_len = len(words) # not sure if there should be some modification on length
	perplexity = 1/(pow(sentprob, 1.0/sent_len))
	print(str(perplexity), file=output_file)
f.close()
output_file.close()

# below is the code for problem 7
output_file = open('smoothed_generation.txt', 'w')
print(GENERATE(word_index_dict, probs, 'bigram', 10, '<s>'), file=output_file)
output_file.close()