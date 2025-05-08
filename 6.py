import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Lukee verkon tiedostosta
def read_network_from_file(filename="verkko.txt"):
    links = set()
    with open(filename, 'r') as f:
        first_line = f.readline().split()
        num_routers, num_links = int(first_line[0]), int(first_line[1])
        for i in range(num_links):
            line = f.readline().split()
            if len(line) != 3:
                continue
            u, v, cost = map(int, line)
            if u == v or cost <= 0 or u < 0 or v < 0 or u >= num_routers or v >= num_routers:
                continue
            if (u, v) in links or (v, u) in links:
                continue
            links.add((u, v, cost))
    return num_routers, list(links)

# Rakennetaan verkko ja lasketaan reitit Dijkstralla
def build_graph_and_paths(num_nodes, links):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for u, v, w in links:
        G.add_edge(u, v, weight=w)

    routing_paths = {}
    for src in range(num_nodes):
        _, paths = nx.single_source_dijkstra(G, src)
        routing_paths[src] = paths

    return G, routing_paths

# Hae lyhin polku lähteestä kohteeseen
def shortest_path(start, end, routing_paths):
    if start in routing_paths and end in routing_paths[start]:
        return routing_paths[start][end]
    else:
        print("❌ Reittiä ei löytynyt.")
        return []

# Animaation piirto valitulle reitille
def animate_path(G, path):
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots()
    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    edge_path = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color='red', width=2, ax=ax)

    packet_dot, = ax.plot([], [], 'ro', markersize=15)

    def update(frame):
        if frame < len(path):
            x, y = pos[path[frame]]
            packet_dot.set_data([x], [y])
        return packet_dot,

    ani = animation.FuncAnimation(fig, update, frames=len(path)+1, interval=1000, repeat=False)
    plt.title(f"Paketin reitti: {path}")
    plt.show()

# Pääohjelma
def main():
    if not os.path.exists("verkko.txt"):
        print("❌ Tiedostoa 'verkko.txt' ei löytynyt.")
        return

    num_nodes, links = read_network_from_file("verkko.txt")
    G, routing_paths = build_graph_and_paths(num_nodes, links)

    print("\n✅ Verkon rakenne luettu.")
    for u, v, w in links:
        print(f" - {u} <--> {v} (etäisyys {w})")

    try:
        start = int(input("\nAnna lähdesolmu: "))
        end = int(input("Anna kohdesolmu: "))
        if not (0 <= start < num_nodes and 0 <= end < num_nodes):
            raise ValueError()
    except ValueError:
        print("❌ Virheellinen solmun numero.")
        return

    path = shortest_path(start, end, routing_paths)
    if path:
        print(f"✅ Laskettiin reitti: {path}")
        animate_path(G, path)

if __name__ == "__main__":
    main()
