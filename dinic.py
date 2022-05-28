# a kód felépítését tekintve networkx folyam algoritmusainak sablonját vette alapul

from collections import deque
import networkx as nx
from networkx.algorithms.flow.utils import build_residual_network

def dinic(G, s, t, capacity="capacity", residual=None):
    if s not in G:
        raise nx.NetworkXError(f"node {str(s)} not in graph")
    if t not in G:
        raise nx.NetworkXError(f"node {str(t)} not in graph")
    if s == t:
        raise nx.NetworkXError("source and sink are the same node")

    if residual is None:
        R = build_residual_network(G, capacity)
    else:
        R = residual

    # A maradékhálózatban az összes él kapacitását átállítjuk 0-ra
    for u in R:
        for e in R[u].values():
            e["flow"] = 0

    INF = R.graph["inf"]

    level = {}

    def breath_first_search():
        global level
        level = {x: -1 for x in R.nodes()}
        queue = deque([s])
        level[s] = 0
        while queue:
            u = queue.popleft()
            for v in R[u]:
                attr = R[u][v]
                if level[v] == -1 and attr["capacity"] - attr["flow"] > 0:
                    level[v] = level[u] + 1
                    queue.append(v)
                    if level[t] != -1 and level[v] == level[t] and t != v:
                        return level
        return level

    def dfs(v, next, flow):
        global level
        if v == t:
            return flow
        numEdges = len(R[v])
        while next[v] < numEdges:
            u = list(R[v])[next[v]]
            attr = R[v][u]
            cap = attr["capacity"] - attr["flow"]
            if cap > 0 and level[u] == level[v] + 1:
                bottleNeck = dfs(u, next, min(flow, cap))
                if bottleNeck > 0:
                    R[v][u]["flow"] += bottleNeck
                    R[u][v]["flow"] -= bottleNeck
                    return bottleNeck

            next[v] += 1

        return 0


    flow_value = 0
    level = breath_first_search()
    while level[t] != -1:
        next = {x: 0 for x in R.nodes()}
        f = dfs(s, next, INF)
        while f != 0:
            flow_value += f
            f = dfs(s, next, INF)
            if flow_value * 2 > INF:
                raise nx.NetworkXUnbounded("Infinite capacity path, flow unbounded above.")
        level = breath_first_search()

    R.graph["flow_value"] = flow_value
    return R
