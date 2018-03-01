#
# To run:
#
# python lev.py <dirname> <lower-threshold> <upper-threshold>
#
# Usage: lev.py directory lower upper
#
import os, sys

#
# https://www.python-course.eu/levenshtein_distance.php
#

#
# recursive
#
memo = { }
def Lev_r(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    cost = 0 if s[-1] == t[-1] else 1
    i1 = (s[:-1], t)
    if not i1 in memo:
        memo[i1] = Lev_r(*i1)
    i2 = (s, t[:-1])
    if not i2 in memo:
        memo[i2] = Lev_r(*i2)
    i3 = (s[:-1], t[:-1])
    if not i3 in memo:
        memo[i3] = Lev_r(*i3)
    res = min([memo[i1]+1, memo[i2]+1, memo[i3]+cost])
    return res

#
# iterative
#
def iterative_levenshtein(s, t):
    """ 
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t
    """
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution
    #for r in range(rows):
    #    print(dist[r])
    return dist[row][col]

#
# Do file-based Lev
#
def LevFile(file1, file2):
	try:
		with open(file1, 'r') as file1_stream:
			content1 = file1_stream.read()
	except IOError:
		print "Could not read ", file1

	try:
		with open(file2, 'r') as file2_stream:
			content2 = file2_stream.read()
	except IOError:
		print "Could not read ", file2

	print "%s (%d) --> %s (%d)" % (file1, len(content1), file2, len(content2))

	#return Lev_r(content1, content2)
	return iterative_levenshtein(content1, content2)

#
# Cluster matrix
#
clus_dic = { }
clus_class = [ ]
all_files = [ ]

def printClusterMatrix():
	global clus_dic
	print "Cluster matrix: "
	for x in clus_dic.keys():
		print x, clus_dic[x]

def doLevClusterMatrix(dirname):
	global all_files, clus_dic
	if os.path.exists(dirname) == False:
		print "Directory %s does not exist"
		return

	# get files
	for filename in os.listdir(dirname):
		all_files += [filename]

	# form dict
	for f1 in all_files:
		clus_dic[f1] = {}
		for f2 in all_files:
			if f1 != f2:
				clus_dic[f1][f2] = LevFile(dirname+"/"+f1, dirname+"/"+f2)
			else:
				clus_dic[f1][f2] = 0
	printClusterMatrix()

#
# Cluster classification recursive
#
def doLevClusterClassify_r(filename, lower, upper):
	global clus_dic, clus_class
	if filename in clus_class:
		return

	for x in clus_dic[filename]:
		if clus_dic[filename][x] >= int(lower) and clus_dic[filename][x] <= int(upper):
			if x not in clus_class:
				clus_class += [x, filename]
				doLevClusterClassify_r(x, lower, upper)

#
# Cluster classification
#
def doLevClusterClassify(lower, upper):
	global all_files
	for filename in all_files:
		doLevClusterClassify_r(filename, lower, upper)

#
# main
#
if __name__ == '__main__':
	if (len(sys.argv) < 4):
		print "Usage: %s <dirname> <lower-threshold> <upper-threshold>" % sys.argv[0]
		sys.exit(1)
	doLevClusterMatrix(sys.argv[1])
	doLevClusterClassify(sys.argv[2], sys.argv[3])

	print "Cluster classification lower %s, upper %s" % (sys.argv[2], sys.argv[3])
	print clus_class
