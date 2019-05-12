#!/bin/python
import sys
from matroids import PartitionMatroid, GraphicMatroid

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

