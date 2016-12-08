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
    start_time = time.time()

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
                print("--- %s seconds ---" % (time.time() - start_time))
                return path, len(path)-2


def score_check(inlist): # werkt nog niet

    Score_front = 0
    Score_end = 0

    for i in inlist:
        if inlist[i] == i + 1:
            Score_front += 1
        else:
            break
    for i in inlist:
        if inlist[(len(inlist) - i - 1)] == len(inlist) - i:
            Score_end += 1
        else:
            break

    Score_tot = Score_front + Score_end
    return Score_tot

# # todo:
# - max score bijhouden:
# max = 0
# if score > max:
#     max = score
# - hoe 3 keer laten lopen, dan alle children uit queue halen, score berekenen en
# met key/value van score/children tijdelijk opslaan (in temp dict??).
# children die max score/2 of hoger hebben -> opnieuw opslaan (weer de queue?)







genomegoal = [1,2,3,4,5,6,7,8,9,10]
genome = [10,2,1,7,3,5,4,6,9,8]
print bfsalgorithm(genome, genomegoal)
