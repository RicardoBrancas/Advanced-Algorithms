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


def breadth_first_search(G, s, t):
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


def depth_first_search(G, s, t, f=None, path=[]):
    path = path + [s]
    if s == t:
        if f:
            f(path)
    else:
        for e in G[s]:
            depth_first_search(G, e, t, f, path)


def depth_first_search_1(G, s, t, f=None, path=[]):
    path = path + [s]
    if s == t:
        if f:
            f(path)
        for i in range(len(path)-1):
            print("(",path[i], ",", path[i+1], ")")
            G.remove_edge(path[i], path[i+1])
            G.add_edge(path[i+1], path[i])
        print(G)

    else:
        for e in filter(lambda x: G.get_label(x) > G.get_label(s), G[s]):
            depth_first_search_1(G, e, t, f, path)


def shortest_path(G, s, t):
    """ G should be an adjacency list
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


def bipartite_max_flow_unweighted(G, s, t, m):
    """ G should be an adjacency list
        s should be the index of the source
        t should be the index of the sink
        m is the number of elements in the first set
    """

    pairing = [None] * m

    while breadth_first_search(G, s, t):
        depth_first_search_1(G, s, t, lambda x: print(x))

    return pairing


def show_pairing(pairing):
    for i, e in enumerate(pairing):
        print(i + 1, " => ", e)
