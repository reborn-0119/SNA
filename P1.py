import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G = nx.read_weighted_edgelist('bali.txt', create_using=nx.DiGraph())

G_und = G.to_undirected(reciprocal=False)  
deg = dict(G_und.degree())
node_sizes = [50 + 10 * deg[n] for n in G_und.nodes()]

pos = nx.spring_layout(G_und, seed=42)
plt.figure(figsize=(8,6))
nx.draw(G_und, pos, node_size=node_sizes, with_labels=False, alpha=0.7)
plt.title("BALI: unweighted undirected (node size ~ degree)")
plt.show()

in_deg = dict(G.in_degree(weight='weight'))  
out_deg = dict(G.out_degree(weight='weight'))

node_size_in = [20 + 5 * in_deg[n] for n in G.nodes()]
edge_widths = [G[u][v]['weight'] for u,v in G.edges()]

pos = nx.spring_layout(G.to_undirected(), weight='weight', seed=42)
plt.figure(figsize=(8,6))
nx.draw_networkx_nodes(G, pos, node_size=node_size_in)
nx.draw_networkx_edges(G, pos, width=edge_widths, arrowstyle='->', arrows=True)
nx.draw_networkx_labels(G, pos, font_size=8)
plt.title("BALI: weighted directed (node size ~ weighted in-degree)")
plt.show()
