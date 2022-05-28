import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import numpy as np
from dinic import dinic
from dinic_bi import dinic_bi
from dinic_level_memory import level_memory_dinic
from modositott_dinic import skip_layer_dinic

def average_time_test(n, m, rounds = 10):
    G = nx.generators.random_graphs.barabasi_albert_graph(n, m, seed = 548)
    random.seed(8647)
    for u, v in G.edges:
        G[u][v]["capacity"] = random.randint(1,30)
    dinic_time = 0
    dinic_bi_time = 0
    dinic_level_time = 0
    dinic_opt_time = 0
    for _ in range(rounds):
        s, t = random.sample(G.nodes, 2)
        #dinic
        generate_start_time = time.time()
        folyam = dinic(G, s, t, capacity='capacity')
        generate_end_time = time.time()
        dinic_time += generate_end_time - generate_start_time
        del folyam
        #dinic_bi
        generate_start_time = time.time()
        folyam = dinic_bi(G, s, t, capacity='capacity')
        generate_end_time = time.time()
        dinic_bi_time += generate_end_time - generate_start_time
        del folyam
        #dinic_level_mem
        generate_start_time = time.time()
        folyam = level_memory_dinic(G, s, t, capacity='capacity')
        generate_end_time = time.time()
        dinic_level_time += generate_end_time - generate_start_time
        del folyam
        #skip_layer_dinic
        generate_start_time = time.time()
        folyam = skip_layer_dinic(G, s, t, capacity='capacity')
        generate_end_time = time.time()
        dinic_opt_time += generate_end_time - generate_start_time
        del folyam

    dinic_time = round(dinic_time/rounds, 5)
    dinic_bi_time = round(dinic_bi_time/rounds, 5)
    dinic_level_time = round(dinic_level_time/rounds, 5)
    dinic_opt_time = round(dinic_opt_time/rounds, 5)
    return dinic_time, dinic_bi_time, dinic_level_time, dinic_opt_time

df = pd.DataFrame(columns = ["csucsszam", "dinic", "dinic_bi", "dinic_level_mem", "dinic_opt"])
for n in np.logspace(2, 4, num=10, base=10, dtype='int'):
    dinic_time, dinic_bi_time, dinic_level_time, dinic_opt_time = average_time_test(n, 5)
    new_row = {"csucsszam": n, "dinic": dinic_time, "dinic_bi": dinic_bi_time, "dinic_level_mem": dinic_level_time, "dinic_opt": dinic_opt_time}
    df = df.append(new_row, ignore_index=True)

df.to_csv('tablazatok/dinic_valtozatok.csv')

def plot_stat(df):
    Fig, ax = plt.subplots()
    for j in range(len(df["csucsszam"])):
        for i, (mark, color) in enumerate(zip(['s', 'o', 'D', 'v'], ['r', 'g', 'b', 'k'])):
            plt.loglog(df["csucsszam"][j], df.iloc[:,i+1][j], color=color,
                       marker=".",
                       markerfacecolor='None',
                       markeredgecolor=color,
                       linestyle = 'None',
                       label="i")
    plt.legend(["dinic", "kétirányú_dinic", "szintmegjegyző_dinic", "módosított_dinic"], loc = "upper left")
    plt.xlabel('gráf csúcsainak száma')
    plt.ylabel('futásidő (s)')
    plt.savefig('abrak/dinic_valtozatok.png', dpi=500)
    plt.show()


plot_stat(df)