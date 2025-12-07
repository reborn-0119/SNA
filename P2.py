import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# ---- Load real-world network ----
file = r"D:\SEM VII\SNA\Practicals\Datasets\workfrance_edgelist.csv"

df = pd.read_csv(file, header=None)
edges = df.iloc[:, :2].values    # first 2 columns

G = nx.Graph()
G.add_edges_from(edges)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())


# ---- Degree Distribution ----
deg = [d for n, d in G.degree()]
unique_deg = sorted(set(deg))
freq = [deg.count(x) for x in unique_deg]

print("\nDegrees:", deg)
print("Unique Degrees:", unique_deg)
print("Frequency:", freq)

# Plot
plt.plot(unique_deg, freq, marker='o')
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution")
plt.show()


# ---- Local Properties ----
print("\nLocal Clustering Coefficient:")
local_cluster = nx.clustering(G)
for node in list(local_cluster)[:10]:   # print only first 10 for brevity
    print(node, ":", local_cluster[node])


# ---- Global Properties ----
global_cluster = nx.average_clustering(G)
transitivity = nx.transitivity(G)

deg_cent = nx.degree_centrality(G)
close_cent = nx.closeness_centrality(G)
between_cent = nx.betweenness_centrality(G)

print("\nGlobal Clustering Coefficient:", global_cluster)
print("Transitivity:", transitivity)
print("\nDegree Centrality:", list(deg_cent.items())[:5])
print("Closeness Centrality:", list(close_cent.items())[:5])
print("Betweenness Centrality:", list(between_cent.items())[:5])
