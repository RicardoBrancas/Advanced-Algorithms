from typing import List, Set, MutableMapping, Collection, Any


def shortest_path(G: MutableMapping[Any, List[Any]], S: Collection[Any], T: Collection[Any]) -> List[Any]:

    s = "_s"
    t = "_t"

    G[s] = []
    for os in S:
        G[s].append(os)
    for ot in T:
        if ot not in G:
            G[ot] = []
        G[ot].append(t)

    pi = {}

    Q = [s]
    finished = False
    while Q:
        if Q[0] in G:
            for n in G[Q[0]]:
                if n not in pi:
                    pi[n] = Q[0]
                    Q.append(n)
                if n == t:
                    Q = []
                    finished = True
                    break
        Q = Q[1:]

    if not finished:
        return []

    path = []
    n = t
    while pi[n] != s:
        path.append(pi[n])
        n = pi[n]

    return path


class Matroid:

    def __init__(self, ground_set: Set):
        print(ground_set)
        self.e = ground_set

    def mk_bipartite(self, other):
        E1 = self.I
        E2 = self.e - self.I

        xy = [(x, y) for x in E1 for y in E2 if self.is_independent_except_with(x, y)]
        yx = [(y, x) for y in E2 for x in E1 if other.is_independent_except_with(x, y)]

        adj = {}
        for x, y in xy + yx:
            if x not in adj:
                adj[x] = []
            adj[x].append(y)

        return adj

    def intersect(self, other):
        self.reset()
        other.reset()
        while True:
            bipartite = self.mk_bipartite(other)

            X1 = [x for x in self.e if x not in self.I and self.is_independent_with(x)]
            X2 = [x for x in other.e if x not in self.I and other.is_independent_with(x)]

            P = shortest_path(bipartite, X1, X2)

            if P:
                for p in P:
                    if p in self.I:
                        self.remove(p)
                        other.remove(p)
                    else:
                        self.add(p)
                        other.add(p)

            else:
                break

        return self.I

    def reset(self):
        self.I = set()

    def remove(self, elem) -> None:
        raise NotImplementedError()

    def add(self, elem) -> None:
        raise NotImplementedError()

    def is_independent_except_with(self, excp, elem) -> bool:
        raise NotImplementedError()

    def is_independent_with(self, elem) -> bool:
        raise NotImplementedError()

