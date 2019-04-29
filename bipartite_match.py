#!/bin/python
import sys
from algos import *

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
