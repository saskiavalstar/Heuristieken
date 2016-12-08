from __future__ import division
from collections import OrderedDict
import time


def bfsalgorithm(genome, genome_goal):

    # Initial list:
    genome_list = list()
    genome_list.append(genome)

    # Archive to maintain memory of genomes and path
    archive = {}
    archive[tuple(genome)] = None

    # Settings:
    layers_before_filter = 2

    while True:

        for i in range(layers_before_filter):
            # Process defined amount of layers, get a positive return value (algorithm found answer) or continue,
            # if continue, filter the set and repeat.
            genome_list, found = process_layers(genome_list, archive, genome_goal)
            print found

            if found:
                # when return type is a path to a solution, return the path and the length minus none value and end.
                return genome_list, len(genome_list) - 2

        # Filter layers
        genome_list = filter_genomes(genome_list, 0.2)

# Takes a set and returns the best (according to our score formula) fraction.
def filter_genomes(genome_list, fraction_returned):

    filtered_list = list()
    fraction_amount = int(round(len(genome_list) * fraction_returned))
    score_archive = {}
    for genome in genome_list:
        score_archive.setdefault(cluster_score(genome), set()).add(tuple(genome))
    sorted_score = OrderedDict(sorted(score_archive.items()))

    # Return desired list
    score_dict = list(sorted_score.items()[:fraction_amount])
    for score_set in score_dict:
        filtered_list = list()
        for genome in score_set[1]:
            filtered_list.append(list(genome))

    score_archive.clear()
    sorted_score.clear()

    return filtered_list


# Takes in a list of genomes and processes all layers up until a defined layer count.
def process_layers(genome_list, child_archive, goal):

    processed_list = list()
    found = False
    for parent in genome_list:
        children_list = allswaps(parent)
        for child in children_list:
            if tuple(child) not in child_archive:
                child_archive[tuple(child)] = parent
                processed_list.append(child)
            if child == goal:
                path = [child]
                parent = tuple(child)
                while parent != None:
                    parent = child_archive[tuple(parent)]
                    path.append(parent)
                    found = True
                return path, found

    return processed_list, found

def reverse_sublist(lst, start, end):
    # Swaps a subset of an array.
    lst[start:end] = lst[start:end][::-1]
    return lst

def cluster_score(genome):
    cluster_count_fw = 0
    cluster_count_bw = 0
    cluster_cover_fw = 0
    cluster_cover_bw = 0
    in_cluster_fw = False
    in_cluster_bw = False

    # clusterscore forward
    for i in range(len(genome) - 1):
        # onnodig dubbel met de tweede if conditie
        # checks if next element is equal to current element
        if genome[i] != (genome[i + 1] - 1):
            in_cluster_fw = False
        else:
            cluster_cover_fw += 1
        if not in_cluster_fw:
            # wat doet dit stukje?
            if genome[i] == genome[i + 1] - 1:
                in_cluster_fw = True
                cluster_count_fw += 1

    # clusterscore backward
    for i in range(len(genome) - 1):
        if genome[i] != (genome[i + 1] + 1):
            in_cluster_bw = False
        else:
            cluster_cover_bw += 1
        if not in_cluster_bw:
            if genome[i] == genome[i + 1] + 1:
                in_cluster_bw = True
                cluster_count_bw += 1

    # calculates total cover (including the first element of a cluster)
    cluster_cover_fw += cluster_count_fw
    cluster_cover_bw += cluster_count_bw

    # calculates total coverage
    cluster_cover_total = cluster_cover_fw + cluster_cover_bw

    # number of clusters
    cluster_count_all = (len(genome) - cluster_cover_total) + cluster_count_fw + cluster_count_bw

    # calculates score
    score = (cluster_cover_total / cluster_count_all)

    return score

def allswaps(genome):
    # Swaps all items in list and returns all results.
    swappeds = list()
    for i in range((len(genome) - 1)):
        for j in range(i + 1, len(genome)):
            new_list = list(genome[:])
            swapped = reverse_sublist(new_list, i, j + 1)
            swappeds.append(swapped)

    return swappeds


genomegoal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
genome = [23, 1, 2, 11, 24, 22, 19, 6, 10, 7, 25, 20, 5, 8, 18, 12, 13, 14, 15, 16, 17, 21, 3, 4, 9]

genomegoal2 = range(1,18)
genome2 = [4,2,14,13,3,8,15,12,5,16,17,11,7,6,10,1,9]
start_time = time.time()
path, score = bfsalgorithm(genome2, genomegoal2)
print (time.time() - start_time)
for route in path:
    print route
print len(path) - 2

# TODO: Weghalen: deel van child_archive (daarin wordt het path bepaald, dus duizend data die weg kan)
# TODO: Weghalen: score archief.
