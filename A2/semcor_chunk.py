from nltk.corpus import semcor

class semcor_chunk:
	def __init__(self, chunk):
		self.chunk = chunk
	
	#returns the synset if applicable, otherwise returns None
	def get_syn_set(self):
		try:
			synset = self.chunk.label().synset()
			return synset
		except AttributeError:
			try:
				synset = wn.synset(self.chunk.label())
				return synset
			except:
				return None

	#returns a list of the words in the chunk
	def get_words(self):
		try:
			return self.chunk.leaves()
		except AttributeError:
			return self.chunk

# if __name__ == "__main__":
# 	s = semcor.tagged_sents(tag='sem')[0]

# 	for chunk in s:
# 		a = semcor_chunk(chunk)

# 		print a.get_syn_set()

# 	for chunk in s:
# 		a = semcor_chunk(chunk)

# 		print a.get_words()