import numpy
import random

from sklearn.metrics.pairwise import cosine_similarity

class NewSDC:
	def predict(self, onehot_corpus, min_samples, eps, expand_rate, seeds=None):
		delta_eps = eps * expand_rate
		labels = [-1 for i in range(len(onehot_corpus))]
		initials = [-1 for i in range(len(onehot_corpus))]

		clusters = []
		clusters.append([])
		cluster_num = 0

		points = [i for i in range(len(onehot_corpus))]
		while len(points) > 0:
			if seeds == None:
				seed_num = random.choice(points)
				seed = numpy.array(onehot_corpus.iloc[seed_num])
			else:
				if len(seeds) == 0:
					for i, label in enumerate(labels):
						if label == -1:
							labels[i] = 0
							clusters[0].append((i, numpy.array(onehot_corpus.iloc[i])))
					break
				seed_num = -1
				seed = seeds.pop(0)

			sims = cosine_similarity(seed.reshape(1, -1), onehot_corpus)
			eps_neighbors = [i for i, sim in enumerate(sims[0]) if sim >= eps and labels[i] <= 0]
			if len(eps_neighbors) >= min_samples:
				cluster_num += 1
				clusters.append([])
				for point in eps_neighbors:
					labels[point] = cluster_num
					clusters[cluster_num].append(numpy.array(onehot_corpus.iloc[point]))
					
					if point == seed_num:
						initials[point] = 0
					else:
						initials[point] = 1
				points = [i for i in points if i not in eps_neighbors]
			elif seeds == None:
			    labels[seed_num] = 0
			    clusters[0].append((seed_num, seed))
			    points.remove(seed_num)

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
