# a dinic_level_memory.py módosított verziója
# a DFS során azon csúcsokat már nem vizsgáljuk melyek level_s értéke maximális, de level_t értékük -1
from collections import deque
import networkx as nx
from networkx.algorithms.flow.utils import build_residual_network

def skip_layer_dinic(G, s, t, capacity="capacity", residual=None):
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

    R_pred = R.pred

    def breath_first_search(level_s, level_t, act_level_s, act_level_t):
        for x in act_level_s:
            level_s[x] = -1
        for x in act_level_t:
            level_t[x] = -1
        act_level_s = set()
        act_level_s.add(s)
        act_level_t = set()
        act_level_t.add(t)
        q_s = deque([s])
        q_t = deque([t])
        level_s[s] = 0
        level_t[t] = 0
        last_level = False
        while q_s and q_t:
            if last_level == True:
                return level_s, level_t, act_level_s, act_level_t
            if len(q_s) <= len(q_t):
                layer_num = len(q_s)
                for _ in range(layer_num):
                    u = q_s.popleft()
                    for v, attr in R[u].items():
                        if level_s[v] == -1 and attr["flow"] < attr["capacity"]:
                            level_s[v] = level_s[u] + 1
                            act_level_s.add(v)
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
                            act_level_t.add(v)
                            if level_s[v] != -1:
                                last_level = True
                            q_t.append(v)

        if last_level == False:
            return None, None, None, None

        return level_s, level_t, act_level_s, act_level_t

    def dfs(v, next, flow, level_s, level_t, skip_layer):
        if v == t:
            return flow
        numEdges = len(R[v])
        while next[v] < numEdges:
            u = list(R[v])[next[v]]
            attr = R[v][u]
            cap = attr["capacity"] - attr["flow"]
            if cap > 0 and ((level_s[v] != -1 and level_s[u] == level_s[v] + 1) or (level_t[u] == level_t[v] - 1))\
                    and (level_s[u] != skip_layer or level_t[u] != -1):
                bottleNeck = dfs(u, next, min(flow, cap), level_s, level_t, skip_layer)
                if bottleNeck > 0:
                    R[v][u]["flow"] += bottleNeck
                    R[u][v]["flow"] -= bottleNeck
                    return bottleNeck

            next[v] += 1

        return 0


    flow_value = 0
    level_s ={}
    level_t = {}
    level_s, level_t, act_s, act_t = breath_first_search(level_s, level_t, R.nodes(), R.nodes())
    while level_s != None:
        next = {x: 0 for x in R.nodes()}
        skip_layer = max(level_s.values())
        f = dfs(s, next, INF, level_s, level_t, skip_layer)
        while f != 0:
            flow_value += f
            f = dfs(s, next, INF, level_s, level_t, skip_layer)
            if flow_value * 2 > INF:
                raise nx.NetworkXUnbounded("Infinite capacity path, flow unbounded above.")
        level_s, level_t,  act_s, act_t = breath_first_search(level_s, level_t, act_s, act_t)

    R.graph["flow_value"] = flow_value
    return R


# Példa a függvény használatára
"""G = nx.DiGraph()
G.add_edge("x", "a", capacity=3.0)
G.add_edge("x", "b", capacity=1.0)
G.add_edge("a", "c", capacity=3.0)
G.add_edge("b", "c", capacity=5.0)
G.add_edge("b", "d", capacity=4.0)
G.add_edge("d", "e", capacity=2.0)
G.add_edge("c", "y", capacity=2.0)
G.add_edge("e", "y", capacity=3.0)
R = skip_layer_dinic(G, "x", "y")
print(R.graph["flow_value"])  # A maximális folyam értéke
"""