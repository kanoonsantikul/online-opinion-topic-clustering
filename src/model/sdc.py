import numpy
import random

from sklearn.metrics.pairwise import cosine_similarity

class SDC:
    def predict(self, onehot_corpus, min_samples, eps):
        delta_eps = eps / 20
        labels = [-1 for i in range(len(onehot_corpus))]
        initials = [-1 for i in range(len(onehot_corpus))]
        sims = cosine_similarity(onehot_corpus)

        points = [i for i in range(len(onehot_corpus))]
        cluster_num = 0
        while len(points) > 0:
            seed = random.choice(points)
            eps_neighbors = [i for i, sim in enumerate(sims[seed]) if sim >= eps and labels[i] <= 0]
            if len(eps_neighbors) >= min_samples:
                cluster_num += 1
                for p in eps_neighbors:
                    labels[p] = cluster_num

                    if p == seed:
                        initials[p] = 0
                    else:
                        initials[p] = 1
                points = [i for i in points if i not in eps_neighbors]
            else:
                labels[seed] = 0
                points.remove(seed)

        while cluster_num != 0:
            cluster = [numpy.array(onehot_corpus.iloc[i]) for i, label in enumerate(labels) if label == cluster_num]
            eps_temp = eps

            while True:
                centroid = numpy.mean(cluster, axis=0).reshape(1, -1)
                eps_temp -= delta_eps

                count = 0
                for i, label in enumerate(labels):
                    point = numpy.array(onehot_corpus.iloc[i]).reshape(1, -1)
                    if label == 0 and cosine_similarity(centroid, point) >= eps_temp:
                        cluster.append(point[0])
                        labels[i] = cluster_num
                        count += 1
                if count == 0:
                    break

            cluster_num -= 1

        return labels, initials
