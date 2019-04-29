from typing import List, Set, Mapping


def shortest_path(G: Mapping[int, List[int]], S: Set[int], T: Set[int]) -> List[int]:
    """ G should be an adjacency list:
        s should be the index of the source
        t should be the index of the sink
    """
    pi = [None] * len(G)

    Q = [s]
    finished = False
    while Q:
        for n in G[Q[0]]:
            if pi[n] is None:
                pi[n] = Q[0]
                Q.append(n)
            if n == t:
                Q = []
                finished = True
                break
        Q = Q[1:]

    if not finished:
        return False

    path = []
    n = t
    while n != s:
        path.append((pi[n], n))
        n = pi[n]

    return path


class Matroid:

    def __init__(self, ground_set: Set, f: Set):
        self.e = ground_set
        self.f = f

    def mk_bipartite(self, other):
        I = self.f & other.f

        E1 = I
        E2 = self.e - I

        xy = [(x, y) for x in E1 for y in E2 if self.is_independent(I - {x} | {y})]
        yx = [(y, x) for y in E2 for x in E1 if other.is_independent(I - {x} | {y})]

        adj = {}
        for x, y in xy + yx:
            if x not in adj:
                adj[x] = []
            adj[x].append(y)

        return adj

    def union(self, other):

        I = set()
        while True:
            bipartite = self.mk_bipartite(other)

            X1 = [x for x in self.e if x not in I and self.is_independent(I | {x})]
            X2 = [x for x in other.e if x not in I and other.is_independent(I | {x})]

            P = shortest_path(bipartite, X1, X2)

            if P:
                I = I ^ set(P)
            else:
                break

        return I

    def is_independent(self, subset) -> bool:
        return subset in self.f


class MaximumSpanningTree(Matroid):

    def __init__(self, V, E):


        super().__init__(V, )


def is_acyclic(graph: List[List[int]], start: int) -> bool:
    visited = []
    stack = [start]
    while stack:
        v = stack[-1]
        visited.append(v)
        stack = stack[:-1]

        for u in graph[v]:
            if visited.index(u):
                return False
            stack.append(u)

    return True
