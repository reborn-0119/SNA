import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

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



#Baic Network
pos=nx.circular_layout(G)
nx.draw(G, pos, with_labels = True, node_size = 400, font_color = "white", connectionstyle='arc3, rad = 0.1' )

# Draw edge labels (weights)

nx.draw(G, pos, with_labels = True, node_size = 400, font_color = "white", connectionstyle='arc3, rad = 0.1' )


edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels)
plt.show()


#node sizes
node_sizes = [300*G.degree(n) for n in G.nodes()]

#edge width
edge_width = [G[u][v]['weight'] for u,v in G.edges()]



# final network

nx.draw(G, pos, with_labels = True, node_size = node_sizes, width = edge_width, font_color = "white", connectionstyle = 'arc3, rad = 0.1')
nx.draw_networkx_edge_labels(G, pos, edge_labels)
plt.show()



#Max Dergee
degree_sequence = sorted((d for n, d in G.degree), reverse = True)

print("Degree Sequence : ",degree_sequence)

dmax = max(degree_sequence)
print("Max Degree : ", dmax)

dmin = min(degree_sequence)
print("Min Degree : ", dmin)