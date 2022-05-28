# Leméri a folyam algoritmusok futási idejét egy G gráfon és a mért adatok elmenti egy pandas dataframe-be
import networkx as nx
import pandas as pd
from networkx.algorithms.flow import boykov_kolmogorov
from networkx.algorithms.flow import preflow_push
import random
import time
from dinic import dinic
from modositott_dinic import skip_layer_dinic as modositott_dinic
random.seed(199234)

"""A = mmread('inf-USAir97.mtx')
G = nx.from_scipy_sparse_matrix(A)"""   # a USAir97 hálózat esetén használandó
#G = nx.generators.random_graphs.barabasi_albert_graph(2000, 7) # Barabási-Albert hálózat esetén használandó
G = nx.read_edgelist("fb-pages-tvshow_edges.txt", nodetype=int, delimiter=",") # fb-pages-tvshow_edges.txt

for u, v in G.edges:
    G[u][v]["capacity"] = random.randint(1,30)
s, t = random.sample(G.nodes, 2)

av_degree = 2*len(G.edges)/len(G.nodes)
low_deg_nodes = []
high_deg_nodes = []

for v in G.nodes():
    deg = G.degree[v]
    if deg > av_degree * 0.5 and deg < av_degree * 1.5:
        low_deg_nodes.append(v)
    if deg > av_degree * 10 and deg < av_degree * 100:
        high_deg_nodes.append(v)

low_pairs = []
high_pairs = []
random.seed(2463)
for _ in range(10):
    u, v = random.sample(low_deg_nodes, 2)
    low_pairs.append((u, v))
    w, z = random.sample(high_deg_nodes, 2)
    high_pairs.append((w, z))

df = pd.DataFrame(columns = ["s", "t", "tavolsag", "dinic", "BK", "szintezo", "modositott_dinic"])

for s, t in low_pairs:
    tavolsag = nx.bidirectional_shortest_path(G, s, t)
    #Dinitz
    generate_start_time = time.time()
    dinic_folyam = dinic(G, s, t, capacity='capacity')
    generate_end_time = time.time()
    dinic_time = round(generate_end_time - generate_start_time, 5)
    del dinic_folyam
    #BK
    generate_start_time = time.time()
    bk_folyam = boykov_kolmogorov(G, s, t, capacity='capacity')
    generate_end_time = time.time()
    BK_time = round(generate_end_time - generate_start_time, 5)
    del bk_folyam
    #szintezo
    generate_start_time = time.time()
    szintezo_folyam = preflow_push(G, s, t, capacity='capacity')
    generate_end_time = time.time()
    szintezo_time = round(generate_end_time - generate_start_time, 5)
    del szintezo_folyam
    #modositott dinic
    generate_start_time = time.time()
    modositott_folyam = modositott_dinic(G, s, t, capacity='capacity')
    generate_end_time = time.time()
    mod_dinic_time = round(generate_end_time - generate_start_time, 5)
    del modositott_folyam
    new_row = {"s":s, "t": t, "tavolsag": len(tavolsag), "dinic": dinic_time, "BK": BK_time, "szintezo": szintezo_time, "modositott_dinic": mod_dinic_time}
    #append row to the dataframe
    df = df.append(new_row, ignore_index=True)

#print(df)
df.to_csv('tablazatok/fb-pages-tvshow_low_pairs.csv', index=False)
