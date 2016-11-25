# alle swaps, 2 for loops
import  time
import Queue
from sets import Set
import random

def reverse_sublist(lst,start,end):
    lst[start:end] = lst[start:end][::-1]
    return lst

testshort = [1,2,3,4,5]
testlong = range(1,26)

def allswaps(list_in):
    start_time = time.time()
    # archive = set()
    swappeds = list()
    for i in range((len(list_in)-1)):
        for j in range(i+1, len(list_in)):
            # swap i en j en sla nieuwe array op zonder staat "testarray"
            new_list = list_in[:]
            swapped = reverse_sublist(new_list, i, j+1)
            swappeds.append(swapped)
            # tup = tuple(swapped)
            # archive.add(tup)
    return swappeds

def bfsalgorithm(genome, genomegoal):
    
    q = Queue.Queue()
    archive = {}
    q.put(genome)
    swapcount = 0
    archive[tuple(genome)] = None
    children_check = children_before_check(len(genome), 2)

    # init score checking values
    score_archive = {}
    score_max = 0

    while True:
        i = 0        
        while i < children_check:
            
            parent = q.get()
            children = allswaps(parent)
            parent = tuple(parent)
            
            for child in children:
                i += 1
                if tuple(child) not in archive:
                    archive[tuple(child)] = parent
                    q.put(child)
                if child == genomegoal:
                    path = [child]
                    parent = tuple(child)
                    while parent != None:
                        parent = archive[parent]
                        path.append(parent)
                    return path, len(path)-2
                    
        while q.empty() == False:            
            score_temp, check_child =  score_check(q.get())
            if score_temp > score_max:
                score_max = score_temp
            score_archive.setdefault(score_temp, set( )).add(tuple(check_child))                                                             
        filtered_set = list(score_archive[score_max])
        score_max -= 1
        filtered_set.append(list(score_archive[score_max]))
                            
        for filtered_child in filtered_set:
            q.put(list(filtered_child))
        score_archive.clear()

#def queue_filter
        
def score_check(inlist):

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
    i = 1
    down_sum = 0
    while i < arrlen:
        down_sum += i
        i += 1
    return down_sum ** layers

def cluster_score(inlist):
    for i in range(len(inlist)):
        next_index = i + 1
        if inlist[i] == inlist[next_index]:
            return Null
        #todo
    
    
# # todo:
# children die max score/2 of hoger hebben -> opnieuw opslaan (weer de queue?)




genomegoal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
genome = [10,13,7,16,17,2,3,8,1,15,14,5,9,4,6,11,12]
start_time = time.time()
print bfsalgorithm(genome, genomegoal)
print (time.time() - start_time)


