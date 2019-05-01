#!/bin/python
import sys
from matroids import *


class PartitionMatroid(Matroid):

    def __init__(self, vertices: List, partition: List, edges: List):
        self.vertices = vertices
        self.partition = partition
        super().__init__(set(edges))

    def reset(self):
        super().reset()
        self.counters_from = {e: 0 for e in self.vertices}
        self.counters_to = {e: 0 for e in self.vertices}

    def remove(self, elem) -> None:
        self.I.remove(elem)

        self.counters_from[elem[0]] -= 1
        self.counters_to[elem[1]] -= 1

    def add(self, elem) -> None:
        self.I.add(elem)

        self.counters_from[elem[0]] += 1
        self.counters_to[elem[1]] += 1

    def is_independent_except_with(self, excp, elem) -> bool:
        for e in self.partition:
            if e == elem[0]:
                if self.counters_from[e] + 1 >= 2:
                    return False
            elif e == excp[0]:
                if self.counters_from[e] - 1 >= 2:
                    return False
            elif self.counters_from[e] >= 2:
                return False

            if e == elem[1]:
                if self.counters_to[e] + 1 >= 2:
                    return False
            elif e == excp[0]:
                if self.counters_to[e] - 1 >= 2:
                    return False
            elif self.counters_to[e] >= 2:
                return False

        return True

    def is_independent_with(self, elem) -> bool:
        for e in self.partition:
            if e == elem[0]:
                if self.counters_from[e] + 1 >= 2:
                    return False
            elif self.counters_from[e] >= 2:
                return False

            if e == elem[1]:
                if self.counters_to[e] + 1 >= 2:
                    return False
            elif self.counters_to[e] >= 2:
                return False

        return True


if __name__ == "__main__":
    data = sys.stdin.readlines()

    m, n = map(int, data[0].split())

    A = ["A" + str(i) for i in range(1, m + 1)]
    B = ["B" + str(i) for i in range(1, n + 1)]

    V = A + B

    E = []

    for line in data[1:]:
        nodes = list(map(int, line.split()))
        E.append(("A" + str(nodes[0]), "B" + str(nodes[1])))

    M2 = PartitionMatroid(V, A, E)
    M1 = PartitionMatroid(V, B, E)

    print(M1.intersect(M2))
