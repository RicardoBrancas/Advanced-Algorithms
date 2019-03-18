#!/bin/python
import sys
from algos import *

data = sys.stdin.readlines()

m, n = map(int, data[0].split())
adj = [[] for i in range(m + n + 2)]
assignment = [None] * m

for line in data[1:]:
    nodes = list(map(int, line.split()))
    adj[nodes[0]].append(m + nodes[1])

for i in range(1, m + 1):
    adj[0].append(i)

for i in range(1, n + 1):
    adj[m + i].append(m + n + 1)

show_pairing(bipartite_max_flow_unweighted(adj, 0, m + n + 1, m))
