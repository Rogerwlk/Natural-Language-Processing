import codecs
import numpy as np
from generate import GENERATE


vocab = codecs.open("brown_vocab_100.txt", "r", encoding="utf-16")

#load the indices dictionary
word_index_dict = {}
for i, line in enumerate(vocab):
    #TODO: import part 1 code to build dictionary
    word_index_dict[line.rstrip()] = i

f = codecs.open("brown_100.txt", 'r', encoding = "utf-16")

#TODO: initialize counts to a zero vector
counts = np.zeros(len(word_index_dict), dtype=np.int)
# print (counts)

#TODO: iterate through file and update counts
for line in f:
	words = line.split()
	for w in words:
		w = w.lower()
		if w in word_index_dict:
			counts[word_index_dict[w]] += 1
# print ()
# print (counts)
f.close()

#TODO: normalize and writeout counts. 
probs = counts / np.sum(counts)
# print(probs)
output_file = open('unigram_probs.txt', 'w')
output_file.write(str(probs))
output_file.close()

# below is the code for problem6
f = codecs.open("toy_corpus.txt", 'r', encoding = "utf-16")
output_file = open('unigram_eval.txt', 'w')

for line in f:
	words = line.split()
	sentprob = 1
	for w in words:
		w = w.lower()
		sentprob *= probs[word_index_dict[w]]
	# print(str(sentprob), file=output_file)

	sent_len = len(words)
	perplexity = 1/(pow(sentprob, 1.0/sent_len))
	print(str(perplexity), file=output_file)
f.close()
output_file.close()

# below is the code for problem 7
output_file = open('unigram_generation.txt', 'w')
print(GENERATE(word_index_dict, probs, 'unigram', 10, '<s>'), file=output_file)
output_file.close()