import re, json, string
from document import Document
from reverse_indexer import Indexer
from clustering import ClusterGraph
from base_cluster import BaseCluster

stopwords = set()

def get_stopwords():
	if not stopwords:
		with open('stopwords.txt', 'r', encoding='utf-8') as f:
			for word in f:
				stopwords.update([word.strip()])
	for c in string.punctuation:
		stopwords.update([c])
	return stopwords

def tokenizer(txt, min_len=0, max_len=12):
	tokens = [token.strip() for token in re.findall(r'\w+', txt) if len(token) > min_len and len(token) < max_len]
	stopwords = get_stopwords()
	def test(item):
		nonlocal stopwords
		if item in stopwords:
			return False
		if re.match(r'\d+\.*\d*', item):
			return False
		return True

	return list(filter(test, tokens))

def build_indexer(doc_list):
	indexer = Indexer()
	for i in range(len(doc_list)):
		item = doc_list[i]
		sentences = []
		sentences.append(tokenizer(item['snippet']))
		#sentences.append([word.strip() for word in re.split(r'[-\s,?)(]+', item['snippet']) if word.strip() and word != '...'])
		doc = Document(i, sentences)
		indexer.insert(doc)
	return indexer

def get_categories(doc_list, removed=False):
	indexer = build_indexer(doc_list)
	set_list = []
	words_list = []
	score_list = []
	
	# base clusters
	basecluster = BaseCluster(indexer.get_phrases())
	base_clusters = basecluster.get_base_clusters()
	for words,docset,count,score in base_clusters:
		set_list.append(docset)
		words_list.append(words)
		score_list.append(score)
	
	# merged clusters
	cg = ClusterGraph(set_list)
	clusters = cg.get_clusters(removed)
	# show clusters
	cg.show_clusters()

	categories = []
	for cluster in clusters:
		category = {
			'keywords': [],
			'items': [],
			'score': 0
		}

		docid_set = set()
		words_set = set()
		for i in cluster:
			category['score'] += score_list[i]
			words_id = '-'.join(words_list[i])
			if not words_id in words_set:
				category['keywords'].append(words_list[i])
				words_set.update([words_id])
			for docid in set_list[i]:
				docid_set.update([docid])
		for docid in docid_set:
			category['items'].append(doc_list[docid])
		categories.append(category)
	return sorted(categories, key=lambda item: item['score'], reverse=True)