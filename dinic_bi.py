# a dinic.py módosítot változata, ebben a breath_first_search függvény kétirányú szélességi keresést használ

from collections import deque
import networkx as nx
from networkx.algorithms.flow.utils import build_residual_network

def dinic_bi(G, s, t, capacity="capacity", residual=None):
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

    for u in R:
        for e in R[u].values():
            e["flow"] = 0

    INF = R.graph["inf"]

    level_s = {}
    level_t = {}
    R_pred = R.pred

    def breath_first_search():
        global level_s
        global level_t
        level_s = {x: -1 for x in R.nodes()}
        level_t = {x: -1 for x in R.nodes()}
        q_s = deque([s])
        q_t = deque([t])
        level_s[s] = 0
        level_t[t] = 0
        last_level = False
        while q_s and q_t:
            if last_level == True:
                return level_s, level_t
            if len(q_s) <= len(q_t):
                layer_num = len(q_s)
                for _ in range(layer_num):
                    u = q_s.popleft()
                    for v, attr in R[u].items():
                        if level_s[v] == -1 and attr["flow"] < attr["capacity"]:
                            level_s[v] = level_s[u] + 1
                            if level_t[v] != -1:
                                last_level = True
                            q_s.append(v)
            else:
                layer_num = len(q_t)
                for _ in range(layer_num):
                    u = q_t.popleft()
                    for v, attr in R_pred[u].items():
                        if level_t[v] == -1 and attr["flow"] < attr["capacity"]:
                            level_t[v] = level_t[u] + 1
                            if level_s[v] != -1:
                                last_level = True
                            q_t.append(v)

        if last_level == False:
            return None, None

        return level_s, level_t

    def dfs(v, next, flow):
        global level_s, level_t
        if v == t:
            return flow
        numEdges = len(R[v])
        while next[v] < numEdges:
            u = list(R[v])[next[v]]
            attr = R[v][u]
            cap = attr["capacity"] - attr["flow"]
            if cap > 0 and ((level_s[v] != -1 and level_s[u] == level_s[v] + 1) or (level_t[u] == level_t[v] - 1)):
                bottleNeck = dfs(u, next, min(flow, cap))
                if bottleNeck > 0:
                    R[v][u]["flow"] += bottleNeck
                    R[u][v]["flow"] -= bottleNeck
                    return bottleNeck

            next[v] += 1

        return 0


    flow_value = 0
    level_s, level_t = breath_first_search()
    while level_s != None:
        next = {x: 0 for x in R.nodes()}
        f = dfs(s, next, INF)
        while f != 0:
            flow_value += f
            f = dfs(s, next, INF)
            if flow_value * 2 > INF:
                raise nx.NetworkXUnbounded("Infinite capacity path, flow unbounded above.")
        level_s, level_t = breath_first_search()

    R.graph["flow_value"] = flow_value
    return R