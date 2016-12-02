# alle swaps, 2 for loops
from __future__ import division
from collections import OrderedDict
import  time
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

    # Bugcheck:
    duplicates = 0
    iterations = 0
    
    # Amount of children before each check is executed;
    children_count = children_before_check(genome_length, layers_before_check)

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
                    return path, len(path)-2
                
        # Filter the queue
        filtered_list = queue_filter(q)
        # Iterate over filtered list and put back to queue                    
        for filtered_child in filtered_list:
            q.put(list(filtered_child))


def queue_filter(q):
    # init score checking values
    score_archive = {}
    score_max = 0

    # Empty queue and filter after arbitrary layers and add good-score children back to queue.                   
    while q.empty() == False:            
        score_temp, genome = cluster_score(q.get())
        # Track highest score in order to get best children back from score_archive.
        if score_temp > score_max:
            score_max = score_temp
        score_archive.setdefault(score_temp, set( )).add(tuple(genome))
        ordered_score = OrderedDict(sorted(score_archive.items()))

    filtered_list = list(ordered_score.items()[:50])

    return filtered_list
        
def cluster_score(genome):
    cluster_count = 0
    cluster_cover = 0
    in_cluster = False

    for i in range(len(genome) - 1):
        if genome[i] != (genome[i + 1] - 1):
            in_cluster = False
        else:
            cluster_cover += 1
        if not in_cluster:
            if genome[i + 1] - 2 == genome[i] - 1:
                in_cluster = True
                cluster_count += 1

    cluster_cover += cluster_count
    cluster_count_all = (len(genome) - cluster_cover) + cluster_count
    score = (cluster_cover / cluster_count_all)
    return score, genome


def children_before_check(arrlen, layers):

    # Calculates total children from each unfiltered, unarchived parent with x layers
    down_sum = children_per_parent(arrlen)
    return down_sum ** layers


def children_per_parent(arrlen):

    # Calculates children per parent.
    i = 1
    down_sum = 0
    while i < arrlen:
        down_sum += i
        i += 1
    return down_sum

def reverse_sublist(lst,start,end):
    # Swaps a subset of an array.
    lst[start:end] = lst[start:end][::-1]
    return lst

def allswaps(list_in):

    # Swaps all items in list and returns all results.
    swappeds = list()
    for i in range((len(list_in)-1)):
        for j in range(i+1, len(list_in)):

            new_list = list_in[:]
            swapped = reverse_sublist(new_list, i, j+1)
            swappeds.append(swapped)
            
    return swappeds

genomegoal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
genome = [23,1,2,11,24,22,19,6,10,7,25,20,5,8,18,12,13,14,15,16,17,21,3,4,9]
genome_test = [10,5,7,2,3,1,4,6,9,8]
goal_test = [1,2,3,4,5,6,7,8,9,10]
start_time = time.time()
path, score =  bfsalgorithm(goal_test, genome_test)
print (time.time() - start_time)
#for route in path:
#    print route

# print cluster_score(genome)


# TODO: layers ipv queue
# TODO: achterwaarts de score berekenen
# TODO: randomdeel?
# TODO: een functie die de eerste X aantal onthoudt en dan steeds vergelijkt of de nieuwe inkomende score beter is dan één van die X, alleen die X onthouden.
# TODO: bepalen hoeveel stappen er nog nodig zijn adhv clusteraantal en goede plek
