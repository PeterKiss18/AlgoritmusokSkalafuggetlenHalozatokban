# Ez kód legyártja a "Folyam algoritmusok magas és alacsony fokszámú csúcspárok között" című ábrát

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('tablazatok/flight_low_pairs.csv')


flight_low_df = pd.melt(df[["dinic", "BK", "szintezo", "modositott_dinic"]])
flight_low_df["graf"] = ["inf-USAir97_low"] * len(flight_low_df)

df = pd.read_csv('tablazatok/flight_high_pairs.csv')

flight_high_df = pd.melt(df[["dinic", "BK", "szintezo", "modositott_dinic"]])
flight_high_df["graf"] = ["inf-USAir97_high"] * len(flight_high_df)

df = pd.read_csv('tablazatok/barabasi_low_pairs.csv')
ba2000_low_df = pd.melt(df[["dinic", "BK", "szintezo", "modositott_dinic"]])
ba2000_low_df["graf"] = ["ba2000_low"] * len(ba2000_low_df)

df = pd.read_csv('tablazatok/barabasi_high_pairs.csv')
ba2000_high_df = pd.melt(df[["dinic", "BK", "szintezo", "modositott_dinic"]])
ba2000_high_df["graf"] = ["ba2000_high"] * len(ba2000_high_df)

df = pd.read_csv('tablazatok/fb-pages-tvshow_low_pairs.csv')
fb_pages_low_df = pd.melt(df[["dinic", "BK", "szintezo", "modositott_dinic"]])
fb_pages_low_df["graf"] = ["fb-pages-tvshow_low"] * len(fb_pages_low_df)

df = pd.read_csv('tablazatok/fb-pages-tvshow_high_pairs.csv')
fb_pages_high_df = pd.melt(df[["dinic", "BK", "szintezo", "modositott_dinic"]])
fb_pages_high_df["graf"] = ["fb-pages-tvshow_high"] * len(fb_pages_high_df)

frames = [flight_low_df, flight_high_df, ba2000_low_df, ba2000_high_df, fb_pages_low_df, fb_pages_high_df]

result_df = pd.concat(frames)

plt.figure(figsize=(12,8))
ax = sns.stripplot(data=result_df, x="graf", y="value", hue="variable", dodge=True)
ax.set_xlabel('Vizsgált hálózat', fontsize = 24)
ax.set_ylabel('Futási idő (s)', fontsize = 24)
ax.semilogy()

# grid and size
num_inst = result_df.graf.nunique()
ax.set_xticks([x+0.5 for x in range(0,num_inst-1)], minor=True)
ax.set_xlim(-0.5, num_inst-0.5)
ax.grid(which='minor', axis='x')
ax.grid(which='major', axis='y')

plt.legend(title='algoritmus', loc='upper left', labels=['dinic', 'BK', 'szintező', "módosított dinic"], fontsize=16)
#plt.savefig("abrak/stripplot_abra.png", dpi = 500)
plt.show()