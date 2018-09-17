import codecs
import numpy as np
from sklearn.preprocessing import normalize
from generate import GENERATE
import random

def trigram(current, prev1, prev2, smooth):
	f = codecs.open("brown_100.txt", 'r', encoding = "utf-16")
	count = 0
	total = 0
	for line in f:
		words = line.split()
		prev_words = ['<s>', '<s>']
		for w in words:
			w = w.lower()
			if prev_words[0] == prev1 and prev_words[1] == prev2:
				total += 1
				if w == current:
					count += 1
			prev_words[0] = prev_words[1]
			prev_words[1] = w
	f.close()
	alpha = 0.1
	vocab_size = 813
	if (smooth):
		count += alpha
		total += alpha * vocab_size
	return count/total

print(str(trigram('past', 'in', 'the', False)))
print(str(trigram('past', 'in', 'the', True)))
print(str(trigram('time', 'in', 'the', False)))
print(str(trigram('time', 'in', 'the', True)))
print(str(trigram('said', 'the', 'jury', False)))
print(str(trigram('said', 'the', 'jury', True)))
print(str(trigram('recommended', 'the', 'jury', False)))
print(str(trigram('recommended', 'the', 'jury', True)))
print(str(trigram('that', 'jury', 'said', False)))
print(str(trigram('that', 'jury', 'said', True)))
print(str(trigram(',', 'agriculture', 'teacher', False)))
print(str(trigram(',', 'agriculture', 'teacher', True)))