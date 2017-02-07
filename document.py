class Document(object):
	def __init__(self, docid, sentences):
		self.sentences = sentences
		self.docid = docid

	def get_id(self):
		return self.docid

	def get_sentences(self):
		return self.sentences