from __future__ import division
from collections import OrderedDict
import time



def Solve_genome(genome, genome_goal):

    # Initial lists (downward and upward:
    genome_list_down = list()
    genome_list_down.append(genome)
    genome_list_up = list()
    genome_list_up.append(genome_goal)

    goal_up = genome
    goal_down = genome_goal

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
            genome_list_down, found = process_layers(genome_list_down, archive_down, goal_down)
            genome_list_up, found = process_layers(genome_list_up, archive_up, goal_up)
            if found:
                break

        # Check if lists have a common item, meaning that there is a path between the original genome and the goal genome
        if len(genome_list_down) > len(genome_list_up):
            if len(set(tuple(genome_list_down)).intersection(tuple(genome_list_up))) != 0:
                return set(tuple(genome_list_down)).intersection(tuple(genome_list_up))
        else:
            if len(set(tuple(genome_list_up)).intersection(tuple(genome_list_down))) != 0:
                return set(tuple(genome_list_up)).intersection(tuple(genome_list_down))



        # Filter lists
        genome_list_down = filter_genomes(genome_list_down, 0.1)
        genome_list_up = filter_genomes(genome_list_up, 0.1)

        # Filter Archives
        archive_up = archive_filter(archive_up, genome_list_up)
        archive_down = archive_filter(archive_down, genome_list_down)


# Takes a set and returns the best (according to our score formula) fraction.
def filter_genomes(genome_list, fraction_returned):

    filtered_list = list()
    fraction_amount = int(round(len(genome_list) * fraction_returned))
    score_archive = {}
    for genome in genome_list:
        score_archive.setdefault(cluster_score_down(genome), set()).add(tuple(genome))
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


# Purges the archive
def archive_filter(archive, genome_list):

    new_archive = {}
    for genome in genome_list:
        genome = tuple(genome)
        while genome is not None:
            new_archive[tuple(genome)] = archive[tuple(genome)]
            genome = archive[tuple(genome)]
    return new_archive


# Takes in a list of genomes and processes all layers up until a defined layer count.
def process_layers(genome_list, archive, goal):

    child_archive = archive
    processed_list = list()
    found = False
    for parent in genome_list:
        children_list = allswaps(parent)
        for child in children_list:
            if tuple(child) not in child_archive:
                child_archive[tuple(child)] = parent
                processed_list.append(child)
            if child == goal:
                found = True
                return child, found
    child_archive.clear()
    return processed_list, found


# Reverses a section, this is the lowest level of algorithm functionality
def reverse_sublist(lst, start, end):

    # Swaps a subset of an array.
    lst[start:end] = lst[start:end][::-1]
    return lst


# Calculates the cluster score from the genome's perspective
def cluster_score_down(genome):
    cluster_count_fw = 0
    cluster_count_bw = 0
    cluster_cover_fw = 0
    cluster_cover_bw = 0
    in_cluster_fw = False
    in_cluster_bw = False

    # Cluster score forward
    for i in range(len(genome) - 1):

        # Checks if next element is equal to current element + 1
        if genome[i] != (genome[i + 1] - 1):
            in_cluster_fw = False
        else:
            cluster_cover_fw += 1
        if not in_cluster_fw:
            # While in a cluster, keep going.
            if genome[i] == genome[i + 1] - 1:
                in_cluster_fw = True
                cluster_count_fw += 1

    # Cluster score backward
    for i in range(len(genome) - 1):
        if genome[i] != (genome[i + 1] + 1):
            in_cluster_bw = False
        else:
            cluster_cover_bw += 1
        if not in_cluster_bw:
            if genome[i] == genome[i + 1] + 1:
                in_cluster_bw = True
                cluster_count_bw += 1

    # Calculates total cover (including the first element of a cluster)
    cluster_cover_fw += cluster_count_fw
    cluster_cover_bw += cluster_count_bw

    # Calculates total coverage
    cluster_cover_total = cluster_cover_fw + cluster_cover_bw

    # Number of clusters
    cluster_count_all = (len(genome) - cluster_cover_total) + cluster_count_fw + cluster_count_bw

    # Calculates score
    score = (cluster_cover_total / cluster_count_all)

    return score


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
        if position_in_original_bw != 0:
            left_neighbor = genome_original[position_in_original_bw - 1]
            if genome[i - 1] == left_neighbor:
                clusters -= 1
    return (len(genome) - clusters) / clusters


    return clusters


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

genomegoal2 = range(1,18)
genome2 = [4,2,14,13,3,8,15,12,5,16,17,11,7,6,10,1,9]
start_time = time.time()
print Solve_genome(genome, genomegoal)
print (time.time() - start_time)

# TODO: Weghalen: deel van child_archive (daarin wordt het path bepaald, dus duizend data die weg kan)
# TODO: Weghalen: score archief.
