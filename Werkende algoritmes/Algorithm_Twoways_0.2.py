from __future__ import division
from collections import OrderedDict
import time
import random


def Solve_genome(genome, genome_goal):

    # Initial lists (downward and upward:
    genome_list_down = list()
    genome_list_down.append(genome)
    genome_list_up = list()
    genome_list_up.append(genome_goal)

    goal_up = genome
    goal_down = genome_goal

    layer_count = 0
    # Archive to maintain memory of genomes and path
    archive_down = {}
    archive_down[tuple(genome)] = None
    archive_up = {}
    archive_up[tuple(genome_goal)] = None

    # Settings:
    layers_before_filter = 1

    while True:

        for i in range(layers_before_filter):
            # Process defined amount of layers, get a positive return value (algorithm found answer) or continue,
            # if continue, filter the set and repeat.
            genome_list_down, found = process_layers(genome_list_down, archive_down)
            intersection =  archive_down.viewkeys() & archive_up.viewkeys()

            layer_count += 1
            if intersection:
                path_down = genome_path(next(iter(intersection)), archive_down)
                path_up = genome_path(next(iter(intersection)), archive_up)

                return path_down[::-1] + path_up[1:]

            genome_list_up, found = process_layers(genome_list_up, archive_up)
            intersection =  archive_down.viewkeys() & archive_up.viewkeys()

            layer_count += 1
            if intersection:
                path_down = genome_path(next(iter(intersection)), archive_down)
                path_up = genome_path(next(iter(intersection)), archive_up)

                return path_down[::-1] + path_up[1:]

                # Check if lists have a common item, meaning that there is a path between the original genome and the goal genome

        # Filter lists
        print "before: ", len(genome_list_down)
        genome_list_down = filter_genomes(genome_list_down, goal_down, 0.1)
        print "after: ", len(genome_list_down)
        genome_list_up = filter_genomes(genome_list_up, goal_up, 0.1)

# Takes a point and archives and creates a path to none
def genome_path(genome, archive):

    path = [genome]
    parent = tuple(genome)
    while parent != None:
        parent = archive[tuple(parent)]
        path.append(parent)
    return path

# Takes a set and returns the best (according to our score formula) fraction.
def filter_genomes(genome_list, genome_goal, fraction_returned):

    filtered_list = list()
    fraction_amount = int(round(len(genome_list) * fraction_returned))
    # print "len: " , len(genome_list), " : " , fraction_amount
    # score_archive = {}
    # for genome in genome_list:
    #     score_archive.setdefault(cluster_score(genome, genome_goal), set()).add(tuple(genome))
    # sorted_score = OrderedDict(sorted(score_archive.items()))
    # print sorted_score
    #
    # # Return desired list
    # score_dict = list(sorted_score.items()[:fraction_amount])
    # for score_set in score_dict:
    #     filtered_list = list()
    #     for genome in score_set[1]:
    #         filtered_list.append(list(genome))
    filtered_list = sorted(genome_list, key = lambda g : cluster_score(genome_goal, genome))[::-1]
    return filtered_list[:500]


# Takes in a list of genomes and processes all layers up until a defined layer count.
def process_layers(genome_list, archive):

    processed_list = list()
    found = False
    for parent in genome_list:
        children_list = allswaps(parent)
        for child in children_list:
            if tuple(child) not in archive:
                archive[tuple(child)] = parent
                processed_list.append(child)
    return processed_list, found


# Reverses a section, this is the lowest level of algorithm functionality
def reverse_sublist(lst, start, end):

    # Swaps a subset of an array.
    lst[start:end] = lst[start:end][::-1]
    return lst


# Calculates the cluster score from the goal's perspective
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


# Produces the entire list of children for a genome
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

genomegoal2 = range(1,10)
genome2 = [5,6,7,2,3,4,1,9,8]
start_time = time.time()

path =  Solve_genome(genome, genomegoal)

for step in path:
    print step
print "swaps: " , len(path) - 3

print (time.time() - start_time)

# TODO: Weghalen: deel van child_archive (daarin wordt het path bepaald, dus duizend data die weg kan)
# TODO: Weghalen: score archief.
