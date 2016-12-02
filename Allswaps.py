# alle swaps, 2 for loops

def reverse_sublist(lst,start,end):
    lst[start:end] = lst[start:end][::-1]
    return lst

testarray = [1,2,3,4,5]

def allswaps(array):

    archive = set()

    for i in range((len(array)-1)):
        for j in range(i, len(array)):

            print i,j
            # swap i en j en sla nieuwe array op zonder staat "testarray"
            temp = array
            swapped = reverse_sublist(temp, i, j+1)
            print swapped
            tup = tuple(swapped)
            archive.add(tup)

    print archive

allswaps(testarray)
