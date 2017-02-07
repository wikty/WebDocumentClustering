from phrase_table import PhraseTable
from utils import words2id

class Indexer(object):
	'''
	words -> document set
	'''
	def __init__(self):
		self.indexer = PhraseTable()

	def insert(self, doc):
		self.indexer.update(doc)

	def get_docset(self, words):
		return self.indexer.get_docset(words)

	def get_most_common(self, k=30):
		# document freq top k
		return self.indexer.get_most_common(k)

	def get_phrases(self, k=2):
		return self.indexer.get_phrases(k)