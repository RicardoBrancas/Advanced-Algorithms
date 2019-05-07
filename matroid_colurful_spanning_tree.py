#!/bin/python
import sys
from matroids import PartitionMatroid, GraphicMatroid
from algos import *

data = sys.stdin.readlines()

v = int(data[0])+1
V = list(range(v))
g = Graph(v)

E = []

for line in data[1:]:
    nodes = line.split()
    E.append((int(nodes[0]), int(nodes[1])))
    g.add_edge(int(nodes[0]), int(nodes[1]))

graphic = GraphicMatroid(V, E)
partition = PartitionMatroid(V, V, E)

print(graphic.intersect(partition))

