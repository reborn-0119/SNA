import networkx as nx
G = nx.karate_club_graph()  # classic Zachary's karate club

degree_c = nx.degree_centrality(G)
closeness_c = nx.closeness_centrality(G)
betweenness_c = nx.betweenness_centrality(G)
eigen_c = nx.eigenvector_centrality_numpy(G)
pagerank_c = nx.pagerank(G, alpha=0.85)

def rank_and_print(d, name, k=5):
    print("---", name, "top", k, "---")
    for node, val in sorted(d.items(), key=lambda x: x[1], reverse=True)[:k]:
        print(node, val)
    print()

rank_and_print(degree_c, "Degree Centrality")
rank_and_print(closeness_c, "Closeness Centrality")
rank_and_print(betweenness_c, "Betweenness Centrality")
rank_and_print(eigen_c, "Eigenvector Centrality")
rank_and_print(pagerank_c, "PageRank")
