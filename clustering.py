import networkx
import matplotlib.pyplot as plt

class ClusterGraph(object):
	def __init__(self, set_list, thresold = 0.5):
		self.thresold = thresold
		self.G = networkx.Graph()
		l = len(set_list)
		for i in range(l):
			for j in range(i+1, l):
				set1 = set_list[i]
				set2 = set_list[j]
				if self.similarity(set1, set2):
					self.G.add_edge(i, j)
	
	def similarity(self, set1, set2):
		if len(set1&set2)/len(set1) > self.thresold and len(set1&set2)/len(set2) > self.thresold:
			#print(set1, set2, 'similar')
			return 1
		return 0

	def show_clusters(self):
		networkx.draw(self.G)
		plt.show()

	def remove_articulation_points(self):
		points = networkx.articulation_points(self.G)
		points = set(points)
		G = networkx.Graph()
		edges = self.G.edges()
		edges = [[fm, to] for fm, to in edges if fm not in points and to not in points]
		G.add_edges_from(edges)
		return G

	def get_clusters(self, ap_removed=False):
		G = self.G
		if ap_removed:
			G = self.remove_articulation_points()
		return list(networkx.connected_components(self.G))
