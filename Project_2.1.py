# Louvain Community Detection on email-Eu-core-temporal (Windows path)
# Save this as community_louvain_run.py and run with: python community_louvain_run.py

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# pip install python-louvain
import community as community_louvain   

FILE_PATH = r"D:\SEM VII\SNA\Project\email-Eu-core-temporal.txt"

# ----------------------------------------------------------
# LOAD DATASET (aggregate temporal edges -> weighted undirected graph)
# ----------------------------------------------------------
G = nx.Graph()
with open(FILE_PATH, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) != 3:
            continue
        u, v, t = parts
        if G.has_edge(u, v):
            G[u][v]["weight"] += 1
        else:
            G.add_edge(u, v, weight=1)

print("Loaded graph:")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# ----------------------------------------------------------
# LOUVAIN COMMUNITY DETECTION
# ----------------------------------------------------------
partition = community_louvain.best_partition(G, weight="weight")
modularity = community_louvain.modularity(partition, G, weight="weight")
print("Modularity:", modularity)

# Build community lists
communities = {}
for node, comm in partition.items():
    communities.setdefault(comm, []).append(node)
print("Detected communities:", len(communities))

# ----------------------------------------------------------
# COMMUNITY SUMMARY TABLE (save & print)
# ----------------------------------------------------------
deg = dict(G.degree(weight="weight"))
rows = []
for cid, nodes in communities.items():
    top_nodes = sorted(nodes, key=lambda n: deg[n], reverse=True)[:5]
    rows.append({
        "Community ID": cid,
        "Size": len(nodes),
        "Top Nodes (by degree)": ", ".join(top_nodes)
    })
df = pd.DataFrame(rows).sort_values("Size", ascending=False).reset_index(drop=True)
print("\nTop communities (by size):")
print(df.head(12).to_string(index=False))

# Save
df.to_csv(r"D:\SEM VII\SNA\Project\community_summary_louvain.csv", index=False)
pd.DataFrame(list(partition.items()), columns=["Node", "Community"]) \
  .to_csv(r"D:\SEM VII\SNA\Project\email_communities_louvain.csv", index=False)
print("\nSaved CSVs to D:\\SEM VII\\SNA\\Project\\ (community_summary_louvain.csv, email_communities_louvain.csv)")

# ----------------------------------------------------------
# community sizes (bar chart)
# ----------------------------------------------------------
plt.figure(figsize=(8,4))
plt.bar(df["Community ID"].astype(str), df["Size"])
plt.title("Community Sizes (Louvain)")
plt.xlabel("Community ID")
plt.ylabel("Number of Nodes")
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# network visualization (top-degree subgraph for readability)
# ----------------------------------------------------------
TOP_N = 300
top_nodes = sorted(G.nodes(), key=lambda n: deg[n], reverse=True)[:TOP_N]
subG = G.subgraph(top_nodes).copy()
pos = nx.spring_layout(subG, seed=42)
node_colors = [partition.get(n, -1) for n in subG.nodes()]

plt.figure(figsize=(10,8))
nx.draw_networkx_nodes(subG, pos, node_size=30, node_color=node_colors, cmap="tab20")
nx.draw_networkx_edges(subG, pos, alpha=0.3, width=0.3)
plt.title(f"Louvain Communities (Top {TOP_N} nodes by degree)")
plt.axis("off")
plt.tight_layout()
plt.show()
