from nltk.corpus import wordnet 
from nltk.corpus import semcor
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
	parser = argparse.ArgumentParser(description='Compute the Levenshtein \
		edit distance between the two untagged sentences in the SemCor corpus \
		at those indices.')
	parser.add_argument('index1', help='first sentence index', type=int)
	parser.add_argument('index2', help='second sentence index', type=int)

	args = parser.parse_args()

	return args

# Returns the cost of inserting a word
def ins_cost(word):
    return 1 # not sure in the description it should be len(word)

# Returns the cost of deleting a word
def del_cost(word):
    return 1 # not sure in the description it should be len(word)

# Returns the cost of substituting word1 with word2
def sub_cost(word1, word2):
	return 1 # not sure in the description it should be max(len(word1), len(word2))

if __name__ == '__main__':
	#...TODO Parse arguments and load semcor sentences
	args = parse_command_line()

	l_sentence1 = semcor.sents()[args.index1]
	l_sentence2 = semcor.sents()[args.index2]
	
	# debug
	# l_sentence1 = ['A', 'Z', 'Q', 'R', 'X', 'A']
	# l_sentence2 = ['A', 'Z', 'J', 'Q', 'R', 'Y']

	# TODO print sentence1 and sentence2
	print (' '.join(l_sentence1))
	print (' '.join(l_sentence2))

	n = len(l_sentence1)
	m = len(l_sentence2)

	# Matrix of cost values. TODO initialize the matrix to the correct size
	# Matrix of edit operations corresponding to costs in cmatrix.
	#TODO Set up row and column 0 in accordance with the algorithm
	cmatrix = []
	
	# handle first row
	first_row = [0]
	for i, word in enumerate(l_sentence2):
		first_row.append(1 + first_row[i]) # not sure in the description 1 should be len(word)
	cmatrix.append(first_row)

	# handle rest
	for i in range(1, n + 1):
		row = [0] * (m + 1)
		row[0] = cmatrix[i - 1][0] + 1 # not sure in the description 1 should be len(l_sentence1[i - 1])
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
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			if l_sentence1[i - 1] == l_sentence2[j - 1]:
				cmatrix[i][j] = cmatrix[i - 1][j - 1]
				ematrix[i][j] = '='
			else:
				sub = cmatrix[i - 1][j - 1] + sub_cost(l_sentence1[i - 1], l_sentence2[j - 1])
				delete = cmatrix[i - 1][j] + del_cost(l_sentence1[i - 1])
				insert = cmatrix[i][j - 1] + ins_cost(l_sentence2[j - 1])

				min_val = sub
				oper = 'SUB'
				if min_val > delete:
					min_val = delete
					oper = 'DEL'
				if min_val > insert:
					min_val = insert
					oper = 'INS'
				
				cmatrix[i][j] = min_val
				ematrix[i][j] = oper

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
	print(' '.join(reversed(seq)))