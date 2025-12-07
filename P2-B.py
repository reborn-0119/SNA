import networkx as nx

# directed graph
G = nx.DiGraph()
edges = [
    ("A", "B"), ("A", "C"), ("A", "F"),
    ("B", "E"), ("C", "D"), ("D", "E"), ("F", "B")
]
G.add_edges_from(edges)

# Simple PageRank (power iteration)
def pagerank_simple(G, alpha=0.85, tol=1.0e-6, max_iter=100):

    nodes = list(G.nodes())
    N = len(nodes)
    idx = {n:i for i,n in enumerate(nodes)}

    out_deg = {n: G.out_degree(n, weight=None) for n in nodes}

    r = {n: 1.0 / N for n in nodes}
    teleport = (1.0 - alpha) / N

    for iteration in range(1, max_iter + 1):
        r_new = {n: 0.0 for n in nodes}

        for u in nodes:
            if out_deg[u] == 0:
                
                share = alpha * r[u] / N
                for v in nodes:
                    r_new[v] += share
            else:
                share = alpha * r[u] / out_deg[u]
                for (src, dst) in G.out_edges(u):
                    r_new[dst] += share
        for v in nodes:
            r_new[v] += teleport

        err = sum(abs(r_new[n] - r[n]) for n in nodes)

        r = r_new

        if err < tol:
            print(f"Custom PageRank converged in {iteration} iterations (err={err:.2e})")
            break
    else:
        print(f"Custom PageRank did NOT converge in {max_iter} iterations, last err={err:.2e}")

    return r, iteration, err

# custom pagerank
alpha = 0.85
pr_custom, iters, final_err = pagerank_simple(G, alpha=alpha, tol=1e-6, max_iter=200)

print("\nCustom PageRank scores:")
for n, score in sorted(pr_custom.items(), key=lambda x: x[1], reverse=True):
    print(f"{n}: {score:.6f}")

pr_nx = nx.pagerank(G, alpha=alpha)  # unweighted

print("\nNetworkX PageRank scores:")
for n, score in sorted(pr_nx.items(), key=lambda x: x[1], reverse=True):
    print(f"{n}: {score:.6f}")


# Comparison

print("\nTop-5 comparison (node : custom vs networkx):")
top_nodes = sorted(pr_custom.items(), key=lambda x: x[1], reverse=True)[:5]
for n, _ in top_nodes:
    print(f"{n}: {pr_custom[n]:.6f}  vs  {pr_nx[n]:.6f}  diff={(pr_custom[n]-pr_nx[n]):.2e}")

# L1 difference between the two PR vectors
l1_diff = sum(abs(pr_custom[n] - pr_nx[n]) for n in G.nodes())
print(f"\nL1 difference between custom and NetworkX PageRank: {l1_diff:.2e}")
