class BaseCluster(object):
	def __init__(self, phrases):
		self.phrases = phrases # [[words, docset, count]]
		self.phrases_sorted_by_docset = []
		self.phrases_sorted_by_phrase = []

	def score_by_docset(self):
		stopwords = []
		with open('stopwords-google.txt', 'r', encoding='utf-8') as f:
			for line in f:
				stopwords.append(line.strip())
		
		def score(words, docset, count):
			nonlocal stopwords
			return len(words)*len(set(words)-set(stopwords))
		
		if not self.phrases_sorted_by_docset:
			for words, docset, count in self.phrases:
				sc = score(words, docset, count)
				self.phrases_sorted_by_docset.append([words, docset, count, sc])
			self.phrases_sorted_by_docset = sorted(self.phrases_sorted_by_docset, key=lambda item:item[3], reverse=True)
		return self.phrases_sorted_by_docset

	def score_by_phrase(self, item):
		def score(words, docset, count):
			return count
		if not self.phrases_sorted_by_phrase:
			for words, docset, count in self.phrases:
				sc = score(words, docset, count)
			self.phrases_sorted_by_phrase.append([words, docset, count, sc])
			self.phrases_sorted_by_phrase = sorted(self.phrases_sorted_by_phrase, key=lambda item:item[2], reverse=True)
		return self.phrases_sorted_by_phrase

	def get_base_clusters(self, k=50, by='docset'):
		if by == 'docset':
			return self.score_by_docset()[:k]
		else:
			return self.score_by_phrase()[:k]