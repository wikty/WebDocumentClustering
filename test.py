import re, json
from document import Document
from reverse_indexer import Indexer
from clustering import ClusterGraph
from base_cluster import BaseCluster

def build_indexer():
	indexer = Indexer()
	for i in range(50):
		filename = 'data/test'+str(i)+'.txt'
		with open(filename, 'r', encoding='utf-8') as f:
			sentences = []
			item = json.loads(f.read())
			sentences.append([word.strip() for word in re.split(r'[-\s,?)(]+', item['snippet']) if word.strip() and word != '...'])
			doc = Document(i, sentences)
			indexer.insert(doc)
	return indexer

indexer = build_indexer()


basecluster = BaseCluster(indexer.get_phrases())

base_clusters = basecluster.get_base_clusters()


# test indexer
# print(indexer.get_docset(['transfer', 'protocol']))
# print(indexer.get_docset(['hypertext', 'transfer']))
# print(indexer.get_most_common(100))
# pandoc -t revealjs -s -i --self-contained readme.md -o readme.html

set_list = []
words_list = []
for words, docset, count,score in base_clusters:
	set_list.append(docset)
	words_list.append(words)

cg = ClusterGraph(set_list)
cg.show_clusters()
clusters = cg.get_clusters()

for i, cluster in zip(range(len(clusters)), clusters):
	print('Cluster', i)
	print(cluster)
	# for j in cluster:
	# 	print(words_list[j], end=' ')
	print('')
	print('')