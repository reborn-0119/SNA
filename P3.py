import networkx as nx
n = 1000

# Random graph
p = 0.01
G_er = nx.erdos_renyi_graph(n, p, seed=42)

# Watts-Strogatz
k = 6 
rewire = 0.1
G_ws = nx.watts_strogatz_graph(n, k, rewire, seed=42)

# Barabasi-Albert
m = 3
G_ba = nx.barabasi_albert_graph(n, m, seed=42)

def display(G, name):
    print("----", name, "----")
    print("nodes:", G.number_of_nodes(), "edges:", G.number_of_edges())
    print("avg degree:", sum(dict(G.degree()).values())/G.number_of_nodes())
    print("avg clustering:", nx.average_clustering(G))
    if nx.is_connected(G):
        print("avg shortest path:", nx.average_shortest_path_length(G))
    else:
        # compute on largest component
        comp = max(nx.connected_components(G), key=len)
        sub = G.subgraph(comp)
        print("largest component size:", sub.number_of_nodes())
        print("avg shortest path (largest comp):", nx.average_shortest_path_length(sub))
    print()

display(G_er, "Erdos-Renyi")
display(G_ws, "Watts-Strogatz")
display(G_ba, "Barabasi-Albert")
