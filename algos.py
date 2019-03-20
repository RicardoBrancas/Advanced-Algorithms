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
                G.set_label(n, G.get_label(Q[0])+1)
                Q.append(n)
        Q = Q[1:]

    return found


def dinic_depth_first_search(G, s, t):
    """ Finds a path from s to t by DFS. Reverses all the edges in the path and returns.
        G: a Graph
        s: the origin
        t: the destination

        Complexity: O(V)
          This alorithm takes as many iterations as the depth of the path from s to t.
          This distance is at most the number of vertices in the graph.
    """
    pi = [None] * G.n
    S = [s]
    while S:
        v = S[-1]
        S = S[:-1]
        if v == t: #we have found the target
            break
        for u in G[v]:
            if G.get_label(u) > G.get_label(v):
                pi[u] = v
                S.append(u)
    v = t
    while pi[v] is not None: #reconstruct the path taken and reverse it
        G.remove_edge(pi[v], v)
        G.add_edge(v, pi[v])
        v = pi[v]


def bipartite_max_flow_unweighted(G, s, t, m):
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

    for i, e in enumerate(G.adj[m+1:-1]): #reconstruct the pairing from the residual network
        if 0 < e[0] <= m:
            pairing[e[0]-1] = i+1

    return pairing


def show_pairing(pairing):
    for i, e in enumerate(pairing):
        print(i + 1, " => ", e)
