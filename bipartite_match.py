#!/bin/python

import sys
import math

def shortest_path(G, s, t):
    """ G should be an adjacency list: 
        s should be the index of the source
        t should be the index of the sink
    """
    print("SP:", G)
    pi = [None] * len(G)

    Q = [s]
    finished = False
    while Q:
        for n in G[Q[0]]:
            if pi[n] == None:
                pi[n] = Q[0]
                Q.append(n)
            if n == t:
                Q = []
                finished=True
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
    """ G should be an adjacency list: 
        s should be the index of the source
        t should be the index of the sink
        m is the number of elements in the first set
    """
    
    pairing = [None] * m

    #we don't need to compute the last shortest_path
    p = shortest_path(G, s, t)
    while p:
        print(p)
        cf = 1
        for u, v in p:
            G[u].remove(v)
            G[v].append(u)
            if u > 0 and u <= m:
                pairing[u-1] = v

        p = shortest_path(G, s, t)

    return pairing


data = sys.stdin.readlines()

m, n = map(int, data[0].split())
adj = [[] for i in range(m+n+2)]
assignment = [None] * m

for line in data[1:]:
    nodes = list(map(int, line.split()))
    adj[nodes[0]].append(m + nodes[1])

for i in range(1,m+1):
    adj[0].append(i)

for i in range(1,n+1):
    adj[m+i].append(m+n+1)

#print(shortest_path(adj, 1, 5))
print(list(map(lambda x:x-m, bipartite_max_flow_unweighted(adj, 0, m+n+1, m))))

#print(adj)
#
#for k in range(m):
#    minimum = math.inf
#    minimizer = None
#    for g in range(1, m+1):
#        if len(adj[g]) != 0 and len(adj[g]) < minimum:
#            minimum = len(adj[g])
#            minimizer = g
#            if minimum == 1:
#                break
#
#    print("girl:", minimizer, "boy:", adj[g][0])
#
#    assignment[minimizer-1] = adj[minimizer][0]
#    adj[minimizer] = []
#    for g in range(1, m+1):
#        if assignment[minimizer-1] in adj[g]:
#            adj[g].remove(assignment[minimizer-1])
#
#    print(assignment)
#    print(adj)
#
#print(assignment)
