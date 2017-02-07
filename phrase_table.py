from utils import words2id

class PhraseTable(object):
	def __init__(self, case_sensitive=True):
		self.tbl = {}
		self.len = 0
		self.case_sensitive = case_sensitive

	def update(self, doc):
		docid = doc.get_id()
		for sentence in doc.get_sentences():
			stc = Sentence(sentence)
			for words in stc.ngrams():
				if self.case_sensitive:
					words = [word.lower() for word in words]
				phrase_id = words2id(words)
				if phrase_id not in self.tbl:
					self.tbl[phrase_id] = Phrase(words)
					self.len += 1
				self.tbl[phrase_id].update(docid)

	def get_docset(self, words):
		if self.case_sensitive:
			words = [word.lower() for word in words]
		phrase_id = words2id(words)
		if phrase_id not in self.tbl:
			return set()
		return self.tbl[phrase_id].get_docset()

	def get_tbl(self):
		return [[self.tbl[phrase_id].get_words(), self.tbl[phrase_id].get_docset(), self.tbl[phrase_id].get_count()] for phrase_id in self.tbl]

	def get_most_common(self, k=20):
		return sorted(self.get_tbl(), key=lambda item:item[2], reverse=True)[:k]

	def get_phrases(self, k=2):
		return list(filter(lambda item:len(item[1])>=k, self.get_tbl()))
	
	@property
	def length(self):
		return self.len

	def dump(self):
		for phrase_id in self.tbl:
			self.tbl[phrase_id].dump()

class Phrase(object):
	def __init__(self, words, case_sensitive=True):
		self.case_sensitive = case_sensitive
		if case_sensitive:
			self.words = [word.lower() for word in words]
		else:
			self.words = words
		self.docset = set()
		self.count = 0

	@property
	def length(self):
		return len(self.words)

	def get_docset(self):
		return self.docset

	def get_count(self):
		return self.count

	def get_words(self):
		return self.words

	def update(self, docid):
		self.docset.update([docid])
		self.count += 1

	def dump(self):
		print('Phrase', self.words)
		print('Count', self.count)
		print('DocSet', self.docset)

class Sentence(object):
	def __init__(self, words):
		self.words = words

	def wordlist(self):
		return [[self.words[i]] for i in range(len(self.words))]

	def bigrams(self):
		return [self.words[i:i+2] for i in range(len(self.words)-1)]
	
	def trigrams(self):
		return [self.words[i:i+3] for i in range(len(self.words)-2)]

	def ngrams(self):
		return self.wordlist() + self.bigrams() + self.trigrams()