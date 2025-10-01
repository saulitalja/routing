import networkx as nx
import matplotlib.pyplot as plt

# Luo painotettu verkko (paino simuloi portin prioriteettia tai linkin kustannusta)
G = nx.Graph()
G.add_weighted_edges_from([
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 6),
    ('C', 'E', 10),
    ('D', 'E', 2),
    ('D', 'F', 6),
    ('E', 'F', 3),
])

# Spanning tree (Kruskalin algoritmi)
T = nx.minimum_spanning_tree(G, algorithm="kruskal")

# Piirrä alkuperäinen verkko
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(12, 6))

plt.subplot(121)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1200)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Alkuperäinen verkko")

# Piirrä spanning tree
plt.subplot(122)
nx.draw(T, pos, with_labels=True, node_color='lightgreen', edge_color='black', node_size=1200)
edge_labels = nx.get_edge_attributes(T, 'weight')
nx.draw_networkx_edge_labels(T, pos, edge_labels=edge_labels)
plt.title("Spanning Tree")

plt.tight_layout()
plt.show()
