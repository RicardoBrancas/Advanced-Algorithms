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


class Edge():

    def __init__(self, to, weight):
        self.to = to
        self.weight = weight


class WeightedGraph:

    def __init__(self, n):
        self.adj = [[0 for j in range(n)] for i in range(n)]
        self.n = n

    def __getitem__(self, key):
        return self.adj[key]

    def set_edge(self, i, j, w):
        self.adj[i][j] = -w


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


def shortest_path(G, s, t):
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

    for i, e in enumerate(G.adj[m+1:-1]): #reconstruct the pairing from the residual network
        if 0 < e[0] <= m:
            pairing[e[0]-1] = i+1

    return pairing


def hungarian_method(G: WeightedGraph):
    """ G should be a WeightedGraph
        s should be the index of the source
        t should be the index of the sink
        m is the number of elements in the first set
    """

    m = float("+inf")
    for row in G.adj:
        m = min(m, min(row))

    for i in range(G.n):
        for j in range(G.n):
            G.adj[i][j] -= m

    # Step 1: Subtract row minima O(n^2)
    for i in range(G.n):
        k = min(G.adj[i])
        for j in range(G.n):
            G.adj[i][j] -= k

    # Step 2: Subtract column minima O(n^2)
    for j in range(G.n):
        k = float("+inf")
        for i in range(G.n):
            k = min(k, G.adj[i][j])
        for i in range(G.n):
            G.adj[i][j] -= k

    ghs = 0
    while True: # HOW MANY TIMES??
        ghs += 1
        print(ghs)
        # Step 3: Cover all zeros with a minimum number of lines
        assigned_rows = [None] * G.n
        crossed_columns = [False] * G.n

        for i in range(G.n): # O(n^2)
            for j in range(G.n):
                if G.adj[i][j] == 0 and not crossed_columns[j]:
                    assigned_rows[i] = j
                    crossed_columns[j] = True

        marked_rows = [False] * G.n
        marked_columns = [False] * G.n
        pairing = [None] * G.n
        for i, j in enumerate(assigned_rows): # O(n)
            if j:
                pairing[i] = j+1

        for i in range(G.n): 
            if not assigned_rows[i]:
                marked_rows[i] = True
       
        while True: # O(n^3)
            for i in range(G.n): # O(n^2)
                for j in range(G.n):
                    if marked_rows[i] and G.adj[i][j] == 0 and not marked_columns[j]:
                        marked_columns[j] = True

            for j in range(G.n): # O(n^2)
                for i2 in range(G.n):
                    if assigned_rows[i2] == j:
                        marked_rows[i2] = True

            cont = False
            for i in range(G.n): # O(n^2)
                for j in range(G.n):
                    if marked_rows[i] and G.adj[i][j] == 0 and not marked_columns[j]:
                        cont = True
            if not cont:
                break


        lines = marked_columns.count(True) + marked_rows.count(False)
        #print(list(map(lambda b: not b, marked_rows)))
        #print(marked_columns)
        #print(G.adj)
        #print(lines)
        if lines == G.n:
            break

        # Step 4: Create additional zeros
        k = float("+inf")
        for i in range(G.n): # O(n^2)
            for j in range(G.n):
                if not marked_columns[j] and marked_rows[i]:
                    k = min(k, G.adj[i][j])

        for i in range(G.n): # O(n^2)
            for j in range(G.n):
                if not marked_columns[j] and marked_rows[i]:
                    G.adj[i][j] -= k
                if marked_columns[j] and not marked_rows[i]:
                    G.adj[i][j] += k

        print(G.adj)
        print()

    return pairing


def show_pairing(pairing):
    i = 0
    for e in pairing:
        if e is not None:
            i += 1
    print("Maximum matching", i) #todo weights
    for i, e in enumerate(pairing):
        if e is not None:
            print(i + 1, " => ", e)
