#!/bin/python
import sys
from algos import *

# Solves the unweighted bipartite matching problem
# The input format is as follows:
#   first line:       two numbers representing the number of elements in each partition
#   every other line: a pair of numbers i,j from 1 to n/m representing a connection
#                     between node i of the first partition and node j of the second
#                     partition
# Example:

#5 5
#1 1
#1 2
#1 3
#1 4
#2 2
#3 5
#4 1
#5 1
#5 5

data = sys.stdin.readlines()

m, n = map(int, data[0].split())
g = Graph(m + n + 2)

assignment = [None] * m

for line in data[1:]:
    nodes = list(map(int, line.split()))
    g.add_edge(nodes[0], m+nodes[1])

for i in range(1, m + 1):
    g.add_edge(0, i)

for i in range(1, n + 1):
    g.add_edge(m+i, m+n+1)

unweighted_show_pairing(bipartite_max_flow_unweighted(g, 0, m+n+1, m))
