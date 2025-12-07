import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = [
    ("A", "B", 3),
    ("A", "C", 5),
    ("A", "F", 1),
    ("B", "E", 2),
    ("C", "D", 4),
    ("D", "E", 2),
    ("F", "B", 1)
]
G.add_weighted_edges_from(edges)

deg = dict(G.degree(weight=None))  
node_sizes = [200 + 300 * deg[n] for n in G.nodes()]  

# edge widths proportional to weight
edge_widths = [G[u][v]['weight'] for u, v in G.edges()]

pos = nx.spring_layout(G, weight='weight', seed=42)

plt.figure(figsize=(7,5))
nx.draw(G, pos, with_labels=True, node_size=node_sizes, width=edge_widths,
        arrows=False, font_color='white')
nx.draw_networkx_edge_labels(G, pos, nx.get_edge_attributes(G, 'weight'))
plt.title("Weighted undirected network (node size by degree, edge width by weight)")
plt.show()
