import numpy
import random

from sklearn.metrics.pairwise import cosine_similarity

class UpgradeSDC:
	def predict(self, onehot_corpus, min_samples, eps):
		delta_eps = eps / 20
		labels = [-1 for i in range(len(onehot_corpus))]
		initials = [-1 for i in range(len(onehot_corpus))]

		clusters = []
		clusters.append([])
		cluster_num = 0

		points = [i for i in range(len(onehot_corpus))]
		sims = cosine_similarity(onehot_corpus)
		while len(points) > 0:
			seed = random.choice(points)
			eps_neighbors = [i for i, sim in enumerate(sims[seed]) if sim >= eps and labels[i] <= 0]
			if len(eps_neighbors) >= min_samples:
				cluster_num += 1
				clusters.append([])
				for p in eps_neighbors:
					labels[p] = cluster_num
					clusters[cluster_num].append(numpy.array(onehot_corpus.iloc[p]))
					
					if p == seed:
						initials[p] = 0
					else:
						initials[p] = 1
				points = [i for i in points if i not in eps_neighbors]
			else:
			    labels[seed] = 0
			    clusters[0].append((seed, numpy.array(onehot_corpus.iloc[seed])))
			    points.remove(seed)

		expandable = numpy.zeros(cluster_num + 1)
		while numpy.sum(expandable) != -cluster_num - 1:
			eps -= delta_eps
			count = numpy.zeros(cluster_num + 1)
			for point in clusters[0]:
			    if labels[point[0]] != 0:
			        continue

			    num = point[0]
			    p = point[1].reshape(1, -1)
			    max_sim = 0
			    for c, cluster in enumerate(clusters[1:]):
			        if expandable[c + 1] == -1:
			            continue
			        centroid = numpy.mean(cluster, axis=0).reshape(1, -1)
			        if cosine_similarity(centroid, p) >= max_sim:
			            max_sim = cosine_similarity(centroid, p)
			            if max_sim >= eps:
			                labels[num] = c + 1

			    if labels[num] != 0:
			        count[labels[num]] += 1
			        clusters[labels[num]].append(point[1])

			for i, num in enumerate(count):
			    if num == 0:
			        expandable[i] = -1

		return labels, initials
