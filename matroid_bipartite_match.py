#!/bin/python
import sys
from matroids import PartitionMatroid

# Solves the unweighted bipartite matching problem, using matroid intersection
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

A = ["A" + str(i) for i in range(1, m + 1)]
B = ["B" + str(i) for i in range(1, n + 1)]

V = A + B

E = []

for line in data[1:]:
    nodes = list(map(int, line.split()))
    E.append(("A" + str(nodes[0]), "B" + str(nodes[1])))

M1 = PartitionMatroid(V, A, E)
M2 = PartitionMatroid(V, B, E)

print(M1.intersect(M2))
