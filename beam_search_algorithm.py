"""""
Beam search Algorithm:

    This algorithm can rotate genome sections towards a specified end state. The main function beam_search_clusterscore()
    takes 2 arguments, the genome to start with and the goal genome. It initiates the list needed for beam search
    processing and the archive to retrieve the path afterwards.

    Consequently it runs until a boolean found is turned to true by the processing function process_layers().
    Then it returns all the steps it took to get to the result, as well as the amount of steps total.

"""

from __future__ import division
from collections import OrderedDict
import time


"""""
beam_search_clusterscore()

    Function:
    Takes two genomes and returns the path between them.

    Input:
    genome, a list of integers.
    genomegoal, a list of integers to work towards.

    Output:
    path, a list of lists containing integers, the swapping path between genome and genomegoal.
    path length, the amount of swaps made.

"""


def beam_search_clusterscore(genome, genome_goal):

    # Initial list containing the input genome:
    genome_list = list()
    genome_list.append(genome)

    # Archive to maintain memory of genomes and path retrieval.
    archive = {}
    archive[tuple(genome)] = None

    # Settings (leave this at one, higher than 2 means slower runtime/memory overflows):
    layers_before_filter = 1

    while True:

        # Semi-redundant, used to check for certainty.
        for i in range(layers_before_filter):
            # Process defined amount of layers, get a positive return value (algorithm found answer) or continue,
            # if continue, filter the set and repeat.
            genome_list, found = process_layers(genome_list, archive, genome_goal)

            if found:
                # when return type is a path to a solution, return the path and the length minus none value and end.
                return genome_list, len(genome_list) - 2

        # Filter layers
        genome_list = filter_genomes(genome_list, 0.2)

"""""
filter_genomes()

    Function:
    Takes a list of genomes and returns the most "promising" node according
    to the score function. This is done by storing genomes in a dictionary with their scores and
    then ordering that dictionary.

    Input:
    genome_list, a list of genomes, a layer of sorts.
    fraction returned, the portion of different scores that were generated to be returned.

    Output:
    A genome list that is filtered to contain the most promising node.
"""


def filter_genomes(genome_list, fraction_returned):

    # Initiate the list to fill, calculate the fraction and initiate the score dictionary.
    filtered_list = list()
    fraction_amount = int(round(len(genome_list) * fraction_returned))
    score_archive = {}

    for genome in genome_list:

        # Store every genome with score in a dictionary and order it.
        score_archive.setdefault(cluster_score(genome), set()).add(tuple(genome))
    sorted_score = OrderedDict(sorted(score_archive.items()))

    # Return desired list
    score_dict = list(sorted_score.items()[:fraction_amount])
    for score_set in score_dict:
        filtered_list = list()
        for genome in score_set[1]:
            filtered_list.append(list(genome))

    return filtered_list

"""""
process_layers()

    Function:
    Takes a list of genomes and returns all children of each genome, without duplicates. Checks each child for
    destination reached. If this is true, form a path from the archive and return it together with found = true,
    so the main function knows when to stop. Else it will continue and return the list of children.

    Input:
    genome_list, a list of parents to create children form.
    child_archive, an archive that contains all previously handled children.
    goal, the genome to work towards and which is checked against every child.

    Output:
    processed_list, a list of all children genomes of the parent layer.
    found, a boolean that determines whether the goal is reached.
"""


def process_layers(genome_list, child_archive, goal):

    processed_list = list()
    found = False

    # Generate all children for every parent.
    for parent in genome_list:
        children_list = allswaps(parent)

        # Store each child in the new list and check if they are the goal.
        for child in children_list:
            if tuple(child) not in child_archive:
                child_archive[tuple(child)] = parent
                processed_list.append(child)

            # If the goal is reached return a path.
            if child == goal:
                path = [child]
                parent = tuple(child)
                while parent != None:
                    parent = child_archive[tuple(parent)]
                    path.append(parent)
                    found = True
                return path, found

    return processed_list, found

"""""
reverse_sublist()

    Function:
    Reverses a sublist in a list and returns the list.

    Input:
    lst, a list.
    start, the index to start the swap from.
    end, the end index.

    Output:
    lst, the list with a reversed sublist.
"""


def reverse_sublist(lst, start, end):
    # Swaps a subset of an array.
    lst[start:end] = lst[start:end][::-1]
    return lst

"""""
cluster_score()

    Function:
    Calculates the cluster score for a genome using the amount of clusters and the total area these clusters cover.

    Input:
    genome_in, a genome to be put in.

    Output:
    score, a float that is calculated using the cluster data for a genome.
"""


def cluster_score(genome_in):

    # Add virtual end and start to determine correct order/direction.
    genome = [0] + genome_in + [26]

    # Keep track of all cluster data.
    cluster_count_fw = 0
    cluster_count_bw = 0
    cluster_cover_fw = 0
    cluster_cover_bw = 0

    # Keep track whether you are in a cluster or not.
    in_cluster_fw = False
    in_cluster_bw = False

    # Clusterscore forward
    for i in range(len(genome) - 1):

        # Checks if next element is equal to current element + 1
        if genome[i] != (genome[i + 1] - 1):
            in_cluster_fw = False
        else:
            cluster_cover_fw += 1
        if not in_cluster_fw:
            # If you are not in a cluster continue counting.
            if genome[i] == genome[i + 1] - 1:
                in_cluster_fw = True
                cluster_count_fw += 1

    # Clusterscore backward
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

    # Actual score score
    score = (cluster_cover_total / cluster_count_all)

    return score

"""""
allswaps()

    Function:
    Generates all children for a genome.

    Input:
    genome, the parent genome, from which all genome children are generated.

    Output:
    swappeds, a list of genomes containing all possible swapped genomes from the original parent.
"""


def allswaps(genome):
    # Swaps all items in list and returns all results.
    swappeds = list()
    for i in range((len(genome) - 1)):
        for j in range(i + 1, len(genome)):
            new_list = list(genome[:])
            swapped = reverse_sublist(new_list, i, j + 1)
            swappeds.append(swapped)

    return swappeds

# The original genomes to work from:
genomegoal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
genome = [23, 1, 2, 11, 24, 22, 19, 6, 10, 7, 25, 20, 5, 8, 18, 12, 13, 14, 15, 16, 17, 21, 3, 4, 9]

# A set of demo genomes:
genomegoal2 = range(1,18)
genome2 = [4,2,14,13,3,8,15,12,5,16,17,11,7,6,10,1,9]

# Timer
start_time = time.time()

# Actual execution of code, returning a path and score (steps).
path, score = beam_search_clusterscore(genome, genomegoal)

# Print every step in the path in a clean manner. Print the time it took to calculate.
print (time.time() - start_time)
for route in path:
    print route
print len(path) - 2

