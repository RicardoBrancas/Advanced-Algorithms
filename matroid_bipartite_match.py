#!/bin/python
import sys
from matroids import PartitionMatroid


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
