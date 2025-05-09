import networkx as nx
import matplotlib.pyplot as plt

# ARP-taulun IP-osoitteet
raw_ip_list = [
    "10.10.216.1",
    "10.10.216.42",
    "10.10.216.72",
#    "10.10.216.23",
    "10.10.216.24"
]

def ip_to_int(ip):
    return sum(int(octet) << (8 * i) for i, octet in enumerate(reversed(ip.split('.'))))

def is_multicast_or_broadcast(ip):
    first_octet = int(ip.split('.')[0])
    return (
        (224 <= first_octet <= 239) or
        ip == "255.255.255.255"
    )

# Erotellaan solmut
unicast_ips = [ip for ip in raw_ip_list if not is_multicast_or_broadcast(ip)]
blocked_ips = [ip for ip in raw_ip_list if is_multicast_or_broadcast(ip)]

# Reunat unicastien välillä
edges = []
for i in range(len(unicast_ips)):
    for j in range(i + 1, len(unicast_ips)):
        ip1 = ip_to_int(unicast_ips[i])
        ip2 = ip_to_int(unicast_ips[j])
        weight = abs(ip1 - ip2)
        edges.append((i, j, weight))

# Kruskalin algoritmi
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        self.parent[yr] = xr
        return True

def kruskal(nodes, edges):
    uf = UnionFind(len(nodes))
    edges.sort(key=lambda x: x[2])
    mst = []
    for u, v, weight in edges:
        if uf.union(u, v):
            mst.append((nodes[u], nodes[v], weight))
    return mst

# Laske MST
mst = kruskal(unicast_ips, edges)

# Graafi
G = nx.Graph()

# Solmut
for ip in unicast_ips:
    G.add_node(ip, color='green')
for ip in blocked_ips:
    G.add_node(ip, color='red')

# Kaikki mahdolliset reunat unicastien välillä
for i in range(len(unicast_ips)):
    for j in range(i + 1, len(unicast_ips)):
        ip1 = unicast_ips[i]
        ip2 = unicast_ips[j]
        weight = abs(ip_to_int(ip1) - ip_to_int(ip2))
        G.add_edge(ip1, ip2, weight=weight, style='dotted', color='gray', width=1)

# Korostetaan MST-reunat
for u, v, w in mst:
    G[u][v]['style'] = 'solid'
    G[u][v]['color'] = 'black'
    G[u][v]['width'] = 2

# Käytä spring_layoutia, joka ottaa huomioon painot
pos = nx.spring_layout(G, weight='weight', seed=42, k=0.7, iterations=200)

# Värit, tyylit ja leveydet
node_colors = [G.nodes[n]['color'] for n in G.nodes]
edge_colors = [G[u][v]['color'] for u, v in G.edges]
edge_styles = [G[u][v]['style'] for u, v in G.edges]
edge_widths = [G[u][v]['width'] for u, v in G.edges]

# Piirto
plt.figure(figsize=(12, 8))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

# Piirrä reunat eri tyyleillä
for style in set(edge_styles):
    styled_edges = [(u, v) for u, v in G.edges if G[u][v]['style'] == style]
    styled_colors = [G[u][v]['color'] for u, v in styled_edges]
    styled_widths = [G[u][v]['width'] for u, v in styled_edges]
    nx.draw_networkx_edges(
        G, pos,
        edgelist=styled_edges,
        style=style,
        edge_color=styled_colors,
        width=styled_widths
    )

# Näytä MST-reunojen painot
edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges if G[u][v]['color'] == 'black'}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Spanning Tree")
plt.axis('off')
plt.tight_layout()
plt.show()
