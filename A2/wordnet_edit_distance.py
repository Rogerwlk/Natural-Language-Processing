from nltk.corpus import wordnet 
from nltk.corpus import semcor
from semcor_chunk import semcor_chunk
import argparse

#debug function to print out the matrix
#taken from https://stackoverflow.com/questions/13214809/pretty-print-2d-python-list
def print_matrix(matrix):
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print ('\n'.join(table))

def parse_command_line():
	parser = argparse.ArgumentParser(description='Compute the \
		edit distance between two tagged sentences in the SemCor corpus \
		at input indices using path similarity or Wu-Palmer similarity.')
	parser.add_argument('index1', help='first sentence index', type=int)
	parser.add_argument('index2', help='second sentence index', type=int)
	parser.add_argument('-sim', help='path/Wu-Palmer similarity', type=str,
		choices=['path', 'wup'])

	args = parser.parse_args()

	if not args.sim:
		parser.error('the following option is required: -sim')

	return args

# Returns the cost of inserting a word
def ins_cost(word):
    return 1

# Returns the cost of deleting a word
def del_cost(word):
    return 1

# Returns the cost of substituting word1 with word2
def sub_cost(word1, word2, sim):
	if word1 and word2 and word1 == word2:
		return 0
	if not word1 or not word2:
		return 1
	if sim == 'path':
		similarity = word1.path_similarity(word2)
	elif sim == 'wup':
		similarity = word1.wup_similarity(word2)
	cost = 1 - similarity
	return cost

def wordnet_edit_distance(s1, s2, sim):
	n = len(s1)
	m = len(s2)

	# Matrix of cost values. TODO initialize the matrix to the correct size
	# Matrix of edit operations corresponding to costs in cmatrix.
	#TODO Set up row and column 0 in accordance with the algorithm
	cmatrix = []
	
	# handle first row
	first_row = list(range(m + 1))
	cmatrix.append(first_row)

	# handle rest
	for i in range(1, n + 1):
		row = [0] * (m + 1)
		row[0] = i
		cmatrix.append(row)
	
	# Matrix of edit sequence. TODO initialize the matrix to the correct size
	# Store the operations: '=' (words match), 'INS', 'DEL', 'SUB'
	#TODO Set up row and column 0 in accordance with the algorithm
	ematrix = []

	# handle first row
	first_row = ['INS'] * (m + 1)
	first_row[0] = '='
	ematrix.append(first_row)

	# handle rest
	for i in range(1, n + 1):
		row = ['='] * (m + 1)
		row[0] = 'DEL'
		ematrix.append(row)
	
	# debug
	# print_matrix (cmatrix)
	# print ()
	# print_matrix (ematrix)

	# Populate the matrices with dynamic programming
	# Your solution should include calls to ins_cost(), del_cost(), and sub_cost()
	for i, chunk_i in enumerate(s1):
		synset_i = semcor_chunk(chunk_i).get_syn_set()
		word_i = semcor_chunk(chunk_i).get_words()
		for j, chunk_j in enumerate(s2):
			synset_j = semcor_chunk(chunk_j).get_syn_set()
			word_j = semcor_chunk(chunk_j).get_words()
			if synset_i and synset_j and synset_i == synset_j or\
			not synset_i and not synset_j and word_i == word_j:
				cmatrix[i + 1][j + 1] = cmatrix[i][j]
				ematrix[i + 1][j + 1] = '='
			else:
				sub = cmatrix[i][j] + sub_cost(synset_i, synset_j, sim)
				delete = cmatrix[i][j + 1] + del_cost(synset_i)
				insert = cmatrix[i + 1][j] + ins_cost(synset_j)

				min_val = sub
				oper = 'SUB'
				if min_val > delete:
					min_val = delete
					oper = 'DEL'
				if min_val > insert:
					min_val = insert
					oper = 'INS'
				
				cmatrix[i + 1][j + 1] = min_val
				ematrix[i + 1][j + 1] = oper

	# debug
	# print()
	# print_matrix(cmatrix)
	# print()
	# print_matrix(ematrix)
	# print()

	# Output the minimum cost computed by the edit distance algorithm
	print(cmatrix[n][m])

	# Output the sequence of operation types to be performed on sentence1 that transform 
	# it to sentence2 with minimum cost. Each operation should be followed by its individual cost.
	# E.g., '= 0 = 0 INS 1 = 0 SUB 1 DEL 1' for the Levenshtein distance 
	# if sentence1 is 'A Z Q R X A' and sentence2 is 'A Z J Q R Y'.
	seq = []
	i = n
	j = m
	while i != 0 and j != 0:
		if ematrix[i][j] == '=':
			seq.append('0')
			seq.append('=')
			i -= 1
			j -= 1
		elif ematrix[i][j] == 'SUB':
			seq.append(str(cmatrix[i][j] - cmatrix[i - 1][j - 1]))
			seq.append('SUB')
			i -= 1
			j -= 1
		elif ematrix[i][j] == 'INS':
			seq.append(str(cmatrix[i][j] - cmatrix[i][j - 1]))
			seq.append('INS')
			j -= 1
		elif ematrix[i][j] == 'DEL':
			seq.append(str(cmatrix[i][j] - cmatrix[i - 1][j]))
			seq.append('DEL')
			i -= 1
	seq = ' '.join(reversed(seq))
	print(seq)

if __name__ == '__main__':
	#...TODO Parse arguments and load semcor sentences
	args = parse_command_line()

	l_sentence1 = semcor.sents()[args.index1]
	l_sentence2 = semcor.sents()[args.index2]

	# TODO print sentence1 and sentence2
	print (' '.join(l_sentence1))
	print (' '.join(l_sentence2))

	s1 = semcor.tagged_sents(tag='sem')[args.index1]
	s2 = semcor.tagged_sents(tag='sem')[args.index2]

	wordnet_edit_distance(s1, s2, args.sim)