#!/bin/python
import sys
from algos import *

sys.stdin.reconfigure(encoding="ascii")


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
