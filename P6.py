import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

# ---- load network ----
file = r"D:\SEM VII\SNA\Practicals\Datasets\workfrance_edgelist.csv"
df = pd.read_csv(file, header=None)
edges = df.iloc[:, :2].values
G = nx.Graph()
G.add_edges_from(edges)
nodes = list(G.nodes())

beta = 0.03       # infection probability per infected neighbor per step
gamma = 0.1       # recovery probability per step (for SIR & SIS)
steps = 100
init_frac = 0.02  # initial infected fraction
runs = 10         # average over several runs

def run_SIR(G, beta, gamma, steps, init_frac):
    N = G.number_of_nodes()
    SIR = []
    for run in range(runs):
        state = {n: 'S' for n in G.nodes()}
        # initial infected
        for n in random.sample(nodes, max(1, int(init_frac * N))):
            state[n] = 'I'
        s_counts = []
        for t in range(steps):
            new_state = state.copy()
            for u in G.nodes():
                if state[u] == 'S':
                    # if any neighbor infected, try to infect per-edge
                    infected_neighbors = sum(1 for v in G.neighbors(u) if state[v] == 'I')
                    # probability that u gets infected this step (1 - prob none infect)
                    if infected_neighbors > 0:
                        p_inf = 1 - (1 - beta) ** infected_neighbors
                        if random.random() < p_inf:
                            new_state[u] = 'I'
                elif state[u] == 'I':
                    if random.random() < gamma:
                        new_state[u] = 'R'
            state = new_state
            s_counts.append((sum(1 for x in state.values() if x=='S'),
                             sum(1 for x in state.values() if x=='I'),
                             sum(1 for x in state.values() if x=='R')))
        SIR.append(s_counts)
    # average over runs
    avg = np.mean(SIR, axis=0)
    return np.array(avg)  # shape (steps, 3)

def run_SIS(G, beta, gamma, steps, init_frac):
    N = G.number_of_nodes()
    SIS = []
    for run in range(runs):
        state = {n: 'S' for n in G.nodes()}
        for n in random.sample(nodes, max(1, int(init_frac * N))):
            state[n] = 'I'
        s_counts = []
        for t in range(steps):
            new_state = state.copy()
            for u in G.nodes():
                if state[u] == 'S':
                    infected_neighbors = sum(1 for v in G.neighbors(u) if state[v] == 'I')
                    if infected_neighbors > 0:
                        p_inf = 1 - (1 - beta) ** infected_neighbors
                        if random.random() < p_inf:
                            new_state[u] = 'I'
                elif state[u] == 'I':
                    if random.random() < gamma:
                        new_state[u] = 'S'   # recovered becomes susceptible again
            state = new_state
            s_counts.append((sum(1 for x in state.values() if x=='S'),
                             sum(1 for x in state.values() if x=='I')))
        SIS.append(s_counts)
    avg = np.mean(SIS, axis=0)
    return np.array(avg)  # shape (steps, 2)

# ---- run sims ----
sir_res = run_SIR(G, beta, gamma, steps, init_frac)   # columns S,I,R
sis_res = run_SIS(G, beta, gamma, steps, init_frac)   # columns S,I

# ---- plot results ----
t = np.arange(steps)
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(t, sir_res[:,0], label='Susceptible')
plt.plot(t, sir_res[:,1], label='Infected')
plt.plot(t, sir_res[:,2], label='Recovered')
plt.title("SIR (avg over runs)")
plt.xlabel("Time step")
plt.ylabel("Number of nodes")
plt.legend()

plt.subplot(1,2,2)
plt.plot(t, sis_res[:,0], label='Susceptible')
plt.plot(t, sis_res[:,1], label='Infected')
plt.title("SIS (avg over runs)")
plt.xlabel("Time step")
plt.legend()

plt.tight_layout()
plt.show()

# ---- simple summary print ----
print("Final (SIR) S,I,R:", sir_res[-1].astype(int))
print("Final (SIS) S,I:", sis_res[-1].astype(int))
