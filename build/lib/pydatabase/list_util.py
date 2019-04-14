#returns a list containing the sum of the values of the lists passed in the lists parameter
#each list has the same number of entries
def sumLists(lists):
	return [sum(i) for i in zip(*lists)]

def divideByList(list1,list2):
	return [i/j for i,j in zip(list1,list2)]

#example: input [(1,),(2,)] -> returns [1,2]
def convertTupleListWithOneEmptyValueToList(tl):
	l = []
	for t in tl:
		l.append(t[0])
	return (l)

def convertListToPostGresList(l):
	s = '"{'
	for v in l:
		if len(s)>2:
			s += ','
		s = s + v
	s += '}"'
	return s