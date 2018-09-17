import codecs


word_index_dict = {}

# TODO: read brown_vocab_100.txt into word_index_dict
input_file = codecs.open('brown_vocab_100.txt', mode='r', encoding='utf-16')
for i, line in enumerate(input_file):
	word_index_dict[line.rstrip()] = i
input_file.close()

# TODO: write word_index_dict to word_to_index_100.txt
output_file = open('word_to_index_100.txt', 'w')
output_file.write(str(word_index_dict))
output_file.close()

print(word_index_dict['all'])
print(word_index_dict['resolution'])
print(len(word_index_dict))
