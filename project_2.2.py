
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = r"D:\SEM VII\SNA\Project\email-Eu-core-temporal.txt"

#graph
G = nx.Graph()
with open(FILE_PATH, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            u, v, t = parts
            if G.has_edge(u, v):
                G[u][v]["weight"] += 1
            else:
                G.add_edge(u, v, weight=1)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# ----------------------------------------------------------
# DEGREE CENTRALITY
# ----------------------------------------------------------
deg_cent = nx.degree_centrality(G)
top_deg = sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Degree Centrality Nodes:")
for n, c in top_deg:
    print(n, c)

# ----------------------------------------------------------
# BETWENNESS CENTRALITY
# ----------------------------------------------------------
bet_cent = nx.betweenness_centrality(G, weight="weight", normalized=True)
top_bet = sorted(bet_cent.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Betweenness Centrality Nodes:")
for n, c in top_bet:
    print(n, c)

# ----------------------------------------------------------
# EIGENVECTOR CENTRALITY
# ----------------------------------------------------------
eig_cent = nx.eigenvector_centrality_numpy(G, weight="weight")
top_eig = sorted(eig_cent.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Eigenvector Centrality Nodes:")
for n, c in top_eig:
    print(n, c)

# ----------------------------------------------------------
# PAGERANK
# ----------------------------------------------------------
pr = nx.pagerank(G, weight="weight")
top_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 PageRank Nodes:")
for n, c in top_pr:
    print(n, c)

# ----------------------------------------------------------
# SAVE RESULTS
# ----------------------------------------------------------
df = pd.DataFrame({
    "Node": list(G.nodes()),
    "Degree Centrality": [deg_cent[n] for n in G.nodes()],
    "Betweenness": [bet_cent[n] for n in G.nodes()],
    "Eigenvector": [eig_cent[n] for n in G.nodes()],
    "PageRank": [pr[n] for n in G.nodes()],
})

df.to_csv(r"D:\SEM VII\SNA\Project\centrality_results.csv", index=False)
print("\nSaved: centrality_results.csv")

# ----------------------------------------------------------
# DEGREE CENTRALITY DISTRIBUTION
# ----------------------------------------------------------
plt.figure(figsize=(8,4))
plt.hist(list(deg_cent.values()), bins=40)
plt.title("Degree Centrality Distribution")
plt.xlabel("Degree Centrality")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
#PAGERANK DISTRIBUTION
# ----------------------------------------------------------
plt.figure(figsize=(8,4))
plt.hist(list(pr.values()), bins=40)
plt.title("PageRank Distribution")
plt.xlabel("PageRank")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
