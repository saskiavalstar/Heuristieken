# alle swaps, 2 for loops
import  time
import Queue

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
    while True:
        parent = q.get()
        children = allswaps(parent)
        parent = tuple(parent)
        for child in children:
            if tuple(child) not in archive:
                archive[tuple(child)] = parent
                q.put(child)
            if child == genomegoal:
                path = [child]
                parent = tuple(child)
                while parent != None:
                    parent = archive[parent]
                    path.append(parent)
                return path


genomegoal = [1,2,3,4,5,6,7,8,9,10]
genome = [10,2,1,7,3,5,4,6,9,8]
print bfsalgorithm(genome, genomegoal)
