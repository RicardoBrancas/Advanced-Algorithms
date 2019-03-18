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


def bipartite_max_flow_unweighted(G, s, t, m):
    """ G should be an adjacency list
        s should be the index of the source
        t should be the index of the sink
        m is the number of elements in the first set
    """

    pairing = [None] * m

    # we don't need to compute the last shortest_path
    p = shortest_path(G, s, t)
    while p:
        for u, v in p:
            G[u].remove(v)
            G[v].append(u)
            if 0 < u <= m:
                pairing[u - 1] = v - m

        p = shortest_path(G, s, t)

    return pairing


def show_pairing(pairing):
    for i, e in enumerate(pairing):
        print(i + 1, " => ", e)