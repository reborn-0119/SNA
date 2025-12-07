import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
edges = [
    ("A", "B"), ("A", "C"),
    ("B", "D"), ("C", "D"),
    ("D", "E"), ("E", "A")
]
G.add_edges_from(edges)


# Degree distribution 

deg_values = [d for n, d in G.degree()]      # list of degrees
unique_deg = sorted(set(deg_values))         # possible degree values
freq = [deg_values.count(x) for x in unique_deg]   # count manually

print("Degrees:", deg_values)
print("Unique Degrees:", unique_deg)
print("Frequency:", freq)

# Plot
plt.plot(unique_deg, freq, marker='o')
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution")
plt.show()


# Local Properties
local_cluster = nx.clustering(G.to_undirected())

print("\nLocal Clustering Coefficient (per node):")
for node in local_cluster:
    print(node, ":", local_cluster[node])


# Global Properties
global_cluster_coeff = nx.average_clustering(G.to_undirected())
global_clust2 = nx.transitivity(G.to_undirected())

deg_centrality = nx.degree_centrality(G)
closeness = nx.closeness_centrality(G)
betweenness = nx.betweenness_centrality(G)

print("\nGlobal Clustering Coefficient:", global_cluster_coeff)
print("Transitivity:", global_clust2)

print("\nDegree Centrality:", deg_centrality)
print("Closeness Centrality:", closeness)
print("Betweenness Centrality:", betweenness)
