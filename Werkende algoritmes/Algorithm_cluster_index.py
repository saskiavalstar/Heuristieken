from __future__ import division
from collections import OrderedDict
import time
import random


def bfsalgorithm(genome, genome_goal):

    # Initial list:
    genome_list = list()
    genome_list.append(genome)

    # Archive to maintain memory of genomes and path
    archive = {}
    archive[tuple(genome)] = None

    # Settings:
    layers_before_filter = 1

    while True:

        for i in range(layers_before_filter):
            # Process defined amount of layers, get a positive return value (algorithm found answer) or continue,
            # if continue, filter the set and repeat.
            genome_list, found = process_layers(genome_list, archive, genome_goal)
            if found:
                # when return type is a path to a solution, return the path and the length minus none value and end.
                return genome_list, len(genome_list) - 2

        # Filter layers
        genome_list = filter_genomes(genome_list,genome_goal, 0.5)

# Takes a set and returns the best (according to our score formula) fraction.
def filter_genomes(genome_list, genome_goal, fraction_returned):

    filtered_list = list()
    fraction_amount = int(round(len(genome_list) * fraction_returned))
    score_archive = {}
    for genome in genome_list:
        score_archive.setdefault(cluster_score(genome_goal, genome), set()).add(tuple(genome))
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

def cluster_score(genome_original, genome):

    clusters = len(genome)
    for i in range(len(genome) - 1):
        position_in_original_fw = genome_original.index(genome[i])
        if position_in_original_fw != len(genome) - 1:
            right_neighbor = genome_original[position_in_original_fw + 1]
            if genome[i + 1] == right_neighbor:
                clusters -= 1

    for i in range(1, len(genome)):
        position_in_original_bw = genome_original.index(genome[i])
        if position_in_original_bw != len(genome) - 1:
            left_neighbor = genome_original[position_in_original_bw + 1]
            if genome[i - 1] == left_neighbor:
                clusters -= 1

    return (len(genome) - clusters) / clusters


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

# start_time = time.time()
# path, score = bfsalgorithm(genome, genomegoal)
# print (time.time() - start_time)
# for route in path:
#     print route
# print len(path) - 2
start_time = time.time()
def random_mutations(run_times, genome_len):

    genome_goal = range(1, genome_len + 1)
    genome = range(1, genome_len + 1)
    average_swaplen = 0
    high_swaplen = 0
    low_swaplen = 0
    avg_score = 0
    low_score = 1000000
    high_score = 0

    for i in range(run_times):
        random.shuffle(genome)
        path, score = bfsalgorithm(genome, genome_goal)
        if score > high_score:
            high_score = score
        if score < low_score:
            low_score = score
        avg_score += score
    avg_score /= run_times

    print "Highest swaps: " , high_score
    print "Lowsest swaps: " , low_score
    print "Average swaps: " , avg_score
    return


print random_mutations(100, 25)
print (time.time() - start_time)

# TODO: Weghalen: deel van child_archive (daarin wordt het path bepaald, dus duizend data die weg kan)
# TODO: Weghalen: score archief.
