from typing import List
from utils import *


class Graph:

    def __init__(self, n):
        self.adj = [[] for i in range(n)]
        self.n = n
        self.init_labels()

    def __getitem__(self, key):
        return self.adj[key]

    def add_edge(self, i, j):
        self.adj[i].append(j)

    def remove_edge(self, i, j):
        self.adj[i].remove(j)

    def init_labels(self):
        self.labels = [None] * self.n
        self.labels[0] = 0

    def get_label(self, n):
        return self.labels[n]

    def set_label(self, n, l):
        self.labels[n] = l

    def __str__(self):
        return str(self.adj) + "\n" + str(self.labels)


# class ColourfulGraph(Graph):
#     def __init__(self, n):
#         super().__init__(n)
#         self.colours = {}
#
#     def add_edge(self, i, j, c):
#         super().add_edge(i, j)
#         self.colours[(i, j)] = c
#         self.colours[(j, i)] = c
#
#     def remove_edge(self, i, j):
#         super().remove_edge(i, j)
#         del self.colours[(i, j)]
#         del self.colours[(j, i)]
#
#     def get_color(self, i, j):
#         return self.colours[(i, j)]
#
#     def __str__(self):
#         return str(self.adj) + "\n" + str(self.colours)


class WeightedAssignmentProblem:

    def __init__(self, n):
        self.adj = [[0 for j in range(n)] for i in range(n)]
        self.orig = [[0 for j in range(n)] for i in range(n)]
        self.mask = [[0 for j in range(n)] for i in range(n)]
        self.n = n
        self.row_cover = [False] * n
        self.column_cover = [False] * n

    def set_edge(self, i, j, w):
        self.orig[i][j] = w
        self.adj[i][j] = w

    def make_positive(self):
        m = 0
        for row in self.adj:
            m_row = max(row)
            if m < m_row:
                m = m_row
        for i in range(self.n):
            for j in range(self.n):
                self.adj[i][j] = m - self.adj[i][j]


def dinic_breadth_first_search(G, s, t):
    """ Performs a BFS in graph G, assigning to each node it's depth.
        G: a Graph
        s: the origin
        t: the destination

        Complexity: O(E)
          In the worst case, we have to traverse all edges in the graph.
    """
    G.init_labels()
    Q = [s]
    found = False
    while Q:
        for n in G[Q[0]]:
            if n == t:
                found = True
            if G.get_label(n) is None:
                G.set_label(n, G.get_label(Q[0]) + 1)
                Q.append(n)
        Q = Q[1:]

    return found


def dinic_depth_first_search(G, s, t):
    """ Finds a path from s to t by DFS. Reverses all the edges in the path and returns.
        G: a Graph
        s: the origin
        t: the destination

        Complexity: O(V)
          This algorithm takes as many iterations as the depth of the path from s to t.
          This distance is at most the number of vertices in the graph.
    """
    pi = [None] * G.n
    S = [s]
    while S:
        v = S[-1]
        S = S[:-1]
        if v == t:  # we have found the target
            break
        for u in G[v]:
            if G.get_label(u) > G.get_label(v):
                pi[u] = v
                S.append(u)
    v = t
    while pi[v] is not None:  # reconstruct the path taken and reverse it
        G.remove_edge(pi[v], v)
        G.add_edge(v, pi[v])
        v = pi[v]


def bipartite_max_flow_unweighted(G: Graph, s, t, m):
    """ G should be an adjacency list
        s should be the index of the source
        t should be the index of the sink
        m is the number of elements in the first set

        Complexity: O(E*V^2)
          Each DFS increases the flow by one unit. In the worst case, we will have to run one BFS for each DFS.
          This happens at most |f*| times, corresponding to O(V) iterations.
          In the end we get: O( #iterations * T_BFS * T_DFS) = O(V*E*V) = O(E*V^2)
          In practice however, we will not need to run a BFS for each DFS, nor will each DFS run through all vertices.
    """

    pairing = [None] * m

    while dinic_breadth_first_search(G, s, t):
        while dinic_depth_first_search(G, s, t):
            pass

    for i, e in enumerate(G.adj[m + 1:-1]):  # reconstruct the pairing from the residual network
        if 0 < e[0] <= m:
            pairing[e[0] - 1] = i + 1

    return pairing


def munkres_algorithm(problem: WeightedAssignmentProblem):
    """ G should be a WeightedGraph
        s should be the index of the source
        t should be the index of the sink
        m is the number of elements in the first set
    """

    problem.make_positive()

    # step 1
    for i in range(problem.n):
        k = min(problem.adj[i])
        for j in range(problem.n):
            problem.adj[i][j] -= k

    # step 2
    for r in range(problem.n):
        for c in range(problem.n):
            if problem.adj[r][c] == 0 and not problem.row_cover[r] and not problem.column_cover[c]:
                problem.mask[r][c] = 1
                problem.row_cover[r] = True
                problem.column_cover[c] = True

    problem.row_cover = [False] * problem.n
    problem.column_cover = [False] * problem.n

    step = 3
    funcs = {3: step3, 4: step4, 5: step5, 6: step6}
    while True:
        step = funcs[step](problem)
        if step == 7:
            break

    pairing = [problem.mask[i].index(1) + 1 for i in range(problem.n)]
    return pairing


def step3(g):
    for i in range(g.n):
        for j in range(g.n):
            if g.mask[i][j] == 1:
                g.column_cover[j] = True

    column_count = 0
    for j in range(g.n):
        if g.column_cover[j]:
            column_count += 1

    if column_count >= g.n:
        return 7
    return 4


def step4(g):
    def find_a_zero():
        nonlocal row, col
        r0 = max(row, 0)
        c0 = max(col, 0)

        row = -1
        col = -1
        for r in crange(r0, r0, g.n):
            if not g.row_cover[r]:
                for c in crange(c0, c0, g.n):
                    if not g.column_cover[c] and g.adj[r][c] == 0:
                        row = r
                        col = c
                        return
            c0 = 0

    def find_star_in_row(row):
        for c in range(g.n):
            if g.mask[row][c] == 1:
                return c
        return -1

    row = -1
    col = -1
    while True:
        find_a_zero()
        if row == -1:
            return 6
        else:
            g.mask[row][col] = 2
            c = find_star_in_row(row)
            if c != -1:
                col = c
                g.row_cover[row] = True
                g.column_cover[col] = False
            else:
                g.path_row_0 = row
                g.path_col_0 = col
                return 5


def step5(g: WeightedAssignmentProblem):
    def find_star_in_col(c):
        nonlocal r
        r = -1
        for i in range(g.n):
            if g.mask[i][c] == 1:
                r = i

    def find_prime_in_row(r):
        nonlocal c
        for j in range(g.n):
            if g.mask[r][j] == 2:
                c = j

    def augment_path():
        nonlocal path
        for p in path:
            if g.mask[p[0]][p[1]] == 1:
                g.mask[p[0]][p[1]] = 0
            else:
                g.mask[p[0]][p[1]] = 1

    def clear_covers():
        for r in range(g.n):
            g.row_cover[r] = False
        for c in range(g.n):
            g.column_cover[c] = False

    def erase_primes():
        for r in range(g.n):
            for c in range(g.n):
                if g.mask[r][c] == 2:
                    g.mask[r][c] = 0

    r = -1
    c = -1
    path = [(g.path_row_0, g.path_col_0)]
    done = False
    while not done:
        find_star_in_col(path[-1][1])
        if r > -1:
            path.append((r, path[-1][1]))
        else:
            done = True

        if not done:
            find_prime_in_row(path[-1][0])
            path.append((path[-1][0], c))

    augment_path()
    clear_covers()
    erase_primes()
    return 3


def step6(g: WeightedAssignmentProblem):
    min_val = float("+inf")

    for r in range(g.n):
        if not g.row_cover[r]:
            for c in range(g.n):
                if not g.column_cover[c] and min_val > g.adj[r][c]:
                    min_val = g.adj[r][c]

    for r in range(g.n):
        for c in range(g.n):
            if g.row_cover[r]:
                g.adj[r][c] += min_val
            if not g.column_cover[c]:
                g.adj[r][c] -= min_val

    return 4


def mk_graph(V, E):
    adj = [[] for i in V]
    for e in E:
        adj[e[0]].append(e[1])
    return adj


def is_acyclic(graph: List[List[int]]) -> bool:
    starts = list(map(lambda l: graph.index(l), filter(lambda x: len(x) != 0, graph)))
    while starts:
        visited = []
        stack = [starts[0]]
        while stack:
            v = stack[-1]
            visited.append(v)
            if v in starts:
                starts.remove(v)
            stack = stack[:-1]

            for u in graph[v]:
                if u in visited:
                    return False
                stack.append(u)

    return True


def show_pairing(G, pairing):
    i = 0
    for k, e in enumerate(pairing):
        if e is not None:
            i += G.orig[k][e - 1]

    print("Maximum matching", i)
    for i, e in enumerate(pairing):
        if e is not None:
            print(i + 1, " => ", e)

def unweighted_show_pairing(pairing):
    i = 0
    for k, e in enumerate(pairing):
        if e is not None:
            i += 1 

    print("Maximum matching", i)
    for i, e in enumerate(pairing):
        if e is not None:
            print(i + 1, " => ", e)
