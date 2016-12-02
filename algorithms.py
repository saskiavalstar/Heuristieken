# alle swaps, 2 for loops
import time
import Queue
from sets import Set
import random


def bfsalgorithm(genome, genome_goal):
    # Generify for calculations sake:
    genome_length = len(genome)
    # Queue to get genomes from. Original is put in first.
    q = Queue.Queue()
    q.put(genome)
    # Arcive to maintain memory of genomes and path
    archive = {}
    archive[tuple(genome)] = None

    # Settings:
    layers_before_check = 2

    while True:
        processed_list = process_layers(genome_list, 3)
        filter_score(processed_set, 0.2)
        #-archief bijhouden
        #-dict bijhouden om met beste scoren de genomen terug te vragen

    while True:
        # Track iterations for each layer
        i = 0
        to_next_layer = layers_before_check
        while i < children_count:

            # Get parent value from queue and produce children
            parent = q.get()
            children = allswaps(parent)
            parent = tuple(parent)

            # Check if children are in archive, and add to queue if not.
            for child in children:
                iterations += 1
                i += 1
                if tuple(child) not in archive:
                    archive[tuple(child)] = parent
                    q.put(child)

                # Check if child is goal, if true returns path from archive.
                if child == genome_goal:
                    path = [child]
                    parent = tuple(child)
                    while parent != None:
                        parent = archive[parent]
                        path.append(parent)
                    return path, len(path) - 2

        # Filter the queue
        filtered_list = queue_filter(q)
        # Iterate over filtered list and put back to queue
        for filtered_child in filtered_list:
            q.put(list(filtered_child))


# Takes in a list of genomes and processes all layers up until a defined layer count.
def process_layers(genome_list, layers, child_archive):

    processed_list = list()
    while layers > 1:
        for parent in genome_list:
            children_list = allswaps(parent)
            for child in children_list:
                if tuple(child) not in child_archive:
                    child_archive[tuple(child)] = parent
                    processed_list.append(child)
                if child == genome_goal:
                    path = [child]
                    parent = tuple(child)
                    while parent != None:
                        parent = archive[parent]
                        path.append(parent)
                    return path
        layers -= 1
        process_layers(processed_list, layers, child_archive)
    return processed_list

def queue_filter(q):
    # init score checking values
    score_archive = {}
    score_max = 0

    # Empty queue and filter after arbitrary layers and add good-score children back to queue.
    while q.empty() == False:
        score_temp, check_child = score_check(q.get())

        # Track highest score in order to get best children back from score_archive.
        if score_temp > score_max:
            score_max = score_temp
        score_archive.setdefault(score_temp, set()).add(tuple(check_child))
    filtered_list = list(score_archive[score_max])

    return filtered_list


def score_check(inlist):
    # Calculates score for start and end clusters
    Score_front1 = 0
    Score_end1 = 0

    for i in range(len(inlist)):
        if inlist[i] == i + 1:
            Score_front1 += 1
        else:
            break

    for i in range(len(inlist)):
        if inlist[(len(inlist) - i - 1)] == len(inlist) - i:
            Score_end1 += 1
        else:
            break

    # Incorporates back to front score
    Score_front2 = 0
    Score_end2 = 0

    for i in range(len(inlist)):
        if inlist[i] == len(inlist) - i:
            Score_front2 += 1
        else:
            break

    for i in range(len(inlist)):
        if inlist[(len(inlist) - i - 1)] == i + 1:
            Score_end2 += 1
        else:
            break

    Score_tot = Score_front1 + Score_end1 + Score_end2 + Score_front2
    return Score_tot, inlist


def children_before_check(arrlen, layers):
    # Calculates total children from each unfiltered, unarchived parent with x layers
    down_sum = children_per_parent(arrlen)
    return down_sum ** layers


def cluster_score(inlist):
    # Calculates score for clusters
    for i in range(len(inlist)):
        next_index = i + 1
        if inlist[i] == inlist[next_index]:
            return Null
            # todo


def children_per_parent(arrlen):
    # Calculates children per parent.
    i = 1
    down_sum = 0
    while i < arrlen:
        down_sum += i
        i += 1
    return down_sum


def reverse_sublist(lst, start, end):
    # Swaps a subset of an array.
    lst[start:end] = lst[start:end][::-1]
    return lst


def allswaps(list_in):
    # Swaps all items in list and returns all results.
    swappeds = list()
    for i in range((len(list_in) - 1)):
        for j in range(i + 1, len(list_in)):
            new_list = list_in[:]
            swapped = reverse_sublist(new_list, i, j + 1)
            swappeds.append(swapped)

    return swappeds


genomegoal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
genome = [23, 1, 2, 11, 24, 22, 19, 6, 10, 7, 25, 20, 5, 8, 18, 12, 13, 14, 15, 16, 17, 21, 3, 4, 9]
start_time = time.time()
path, score = bfsalgorithm(genome, genomegoal)
print (time.time() - start_time)
for route in path:
    print route