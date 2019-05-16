#!/bin/python
import sys
from matroids import PartitionMatroid, GraphicMatroid

# Solves the r-arborescence problem using matroid intersection
# The input format is as follows:
#   first line:       the number of vertices
#   second line:      the index of the root, r. There should be no vertices incoming into the root
#   every other line: a pair of numbers i,j from 1 to n/m representing a connection
#                     between node i of the first partition and node j of the second
#                     partition
# Example:

#5
#0
#0 1
#0 3
#0 4
#2 2
#2 4
#3 2
#3 4
#4 1
#4 2


data = sys.stdin.readlines()

v = int(data[0])
r = int(data[1])
V = set(range(v))

E = []

for line in data[2:]:
    nodes = line.split()
    E.append((int(nodes[0]), int(nodes[1])))

graphic = GraphicMatroid(list(V), E)
partition = PartitionMatroid(list(V), list(V - {r}), E, both=False)

print(partition.intersect(graphic))

