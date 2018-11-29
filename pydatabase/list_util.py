#returns a list containing the sum of the values of the lists passed in the lists parameter
#each list has the same number of entries
def sumLists(lists):
	return [sum(i) for i in zip(*lists)]

#example: input [(1,),(2,)] -> returns [1,2]
def convertTupleListWithOneEmptyValueToList(tl):
	l = []
	for t in tl:
		l.append(t[0])
	return (l)