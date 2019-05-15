#!/bin/python
import sys
from algos import *

# Solves the weighted bipartite matching problem
# The input format is as follows:
#   first line:       two numbers representing the number of elements in each partition
#   every other line: a pair of numbers i,j from 1 to n/m representing a connection
#                     between node i of the first partition and node j of the second
#                     partition
#                     followed by another integer representing the weight of that edge
# Example:

#5 5
#1 5 10
#2 1 18
#2 2 14
#2 5 9
#3 5 2
#4 3 16
#4 5 10
#5 2 19
#5 4 9


def read_graph():
    m, n = map(int, sys.stdin.readline().split())
    g = WeightedAssignmentProblem(max(m, n))

    d = sys.stdin.readlines()
    for line in d:
        nodes = line.split()
        g.set_edge(int(nodes[0]) - 1, int(nodes[1]) - 1, int(nodes[2]))

    return g


g = read_graph()
show_pairing(g, munkres_algorithm(g))
