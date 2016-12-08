# alle swaps, 2 for loops
import time

def reverse_sublist(lst,start,end):
    lst[start:end] = lst[start:end][::-1]
    return lst

testshort = [1,2,3,4,5]
testlong = range(1,26)

def allswaps(list_in):
    start_time = time.time()
    archive = set()

    for i in range((len(list_in)-1)):
        for j in range(i+1, len(list_in)):
            # swap i en j en sla nieuwe array op zonder staat "testarray"
            new_list = list_in[:]
            swapped = reverse_sublist(new_list, i, j+1)
            tup = tuple(swapped)
            archive.add(tup)

    print len(archive)
    print("--- %s seconds ---" % (time.time() - start_time))


allswaps(testlong)
