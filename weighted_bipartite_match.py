#!/bin/python
import sys
from algos import *

data = sys.stdin.readlines()

m, n = map(int, data[0].split())
g = WeightedGraph(max(m,n))

assignment = [None] * m

for line in data[1:]:
    nodes = list(map(int, line.split()))
    g.set_edge(nodes[0]-1, nodes[1]-1, nodes[2])

#for i in range(1, m + 1):
#    g.set_edge(0, i, )

#for i in range(1, n + 1):
#    g.set_edge(m+i, m+n+1)

hungarian_method(g)
