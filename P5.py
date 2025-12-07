import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import community as community_louvain
from sklearn.metrics import normalized_mutual_info_score

G = nx.karate_club_graph()

# ground-truth (club: 'Mr. Hi' or 'Officer')
ground_truth = [0 if G.nodes[n]['club']=="Mr. Hi" else 1 for n in G.nodes()]

# Fast Greedy (greedy modularity)
fg_communities = list(greedy_modularity_communities(G))
# map node -> community id
fg_labels = {}
for i,c in enumerate(fg_communities):
    for node in c:
        fg_labels[node] = i
fg_label_list = [fg_labels[n] for n in G.nodes()]

# Louvain
louvain_partition = community_louvain.best_partition(G)  # dict node->community
lv_label_list = [louvain_partition[n] for n in G.nodes()]

# modularity (global quality)
mod_fg = nx.algorithms.community.quality.modularity(G, fg_communities)
# for louvain, convert to list of sets
lv_comms = {}
for n,c in louvain_partition.items():
    lv_comms.setdefault(c, set()).add(n)
lv_communities = list(lv_comms.values())
mod_lv = nx.algorithms.community.quality.modularity(G, lv_communities)

# NMI with ground truth (compare each algorithm's labels to ground truth)
nmi_fg = normalized_mutual_info_score(ground_truth, fg_label_list)
nmi_lv = normalized_mutual_info_score(ground_truth, lv_label_list)

print("Modularity - FastGreedy:", round(mod_fg,4), "Louvain:", round(mod_lv,4))
print("NMI vs ground-truth - FastGreedy:", round(nmi_fg,4), "Louvain:", round(nmi_lv,4))

# draw communities (side-by-side)
pos = nx.spring_layout(G, seed=42)

fig, axs = plt.subplots(1,2,figsize=(10,5))
# colors for FG
colors_fg = [fg_labels[n] for n in G.nodes()]
axs[0].set_title("Fast Greedy communities")
nx.draw_networkx_nodes(G, pos, node_color=colors_fg, cmap=plt.cm.tab10, node_size=200, ax=axs[0])
nx.draw_networkx_edges(G, pos, ax=axs[0])
nx.draw_networkx_labels(G, pos, font_size=8, ax=axs[0])

# colors for Louvain
colors_lv = [louvain_partition[n] for n in G.nodes()]
axs[1].set_title("Louvain communities")
nx.draw_networkx_nodes(G, pos, node_color=colors_lv, cmap=plt.cm.tab10, node_size=200, ax=axs[1])
nx.draw_networkx_edges(G, pos, ax=axs[1])
nx.draw_networkx_labels(G, pos, font_size=8, ax=axs[1])

plt.tight_layout()
plt.show()

# Comparison bar plots: modularity and NMI
plt.figure(figsize=(8,4))
algos = ['FastGreedy','Louvain']
mods = [mod_fg, mod_lv]
plt.subplot(1,2,1)
plt.bar(algos, mods)
plt.title("Modularity")
plt.ylim(0,1)

plt.subplot(1,2,2)
nmis = [nmi_fg, nmi_lv]
plt.bar(algos, nmis)
plt.title("NMI vs Ground-truth")
plt.ylim(0,1)

plt.tight_layout()
plt.show()
