import unicodedata
def normalize(s):
	return unicodedata.normalize("NFKD", s.casefold())
def equalsIgnoreCase(left, right):
	if left==None:
		return False
	if right==None:
		return False
	return normalize(left) == normalize(right)