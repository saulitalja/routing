import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

# Reititystaulun muodostus RIP-tyyliin (next-hop)
def build_routing_table(graph, nodes):
    table = {}
    for src in nodes:
        table[src] = {}
        lengths, paths = nx.single_source_dijkstra(graph, src)
        for dst in nodes:
            if dst == src or dst not in paths:
                continue
            path = paths[dst]
            if len(path) > 1:
                table[src][dst] = path[1]
    return table

# Laske reitti RIP-taulun perusteella
def shortest_path(start, end, table):
    path = [start]
    current = start
    while current != end:
        next_hop = table.get(current, {}).get(end)
        if next_hop is None or next_hop in path:
            print("Reittiä ei löytynyt tai havaittiin silmukka.")
            break
        path.append(next_hop)
        current = next_hop
    return path

# Animaation piirto
def animate_path(G, path):
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)

    # Korostetaan reitti punaisella viivalla
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

# Pääohjelma käyttäjän syötteellä
def main():
    print("Syötä solmujen ja linkkien tiedot (RIP-simulaatio)")
    num_nodes = int(input("Anna solmujen määrä: "))
    G = nx.Graph()
    nodes = list(range(num_nodes))

    print("Syötä yhteydet muodossa: <solmu1> <solmu2> <paino>")
    print("Anna tyhjä rivi lopettaaksesi.")
    while True:
        line = input("Linkki: ")
        if not line.strip():
            break
        u, v, w = map(int, line.strip().split())
        if w <= 0:
            print("Etäisyyden on oltava positiivinen.")
            continue
        G.add_edge(u, v, weight=w)

    routing_table = build_routing_table(G, nodes)

    print("\nRIP-reititystaulut (next-hop):")
    for src in routing_table:
        print(f"{src}: {routing_table[src]}")

    start = int(input("Anna lähdesolmu: "))
    end = int(input("Anna kohdesolmu: "))

    path = shortest_path(start, end, routing_table)
    print("Laskettiin reitti:", path)

    animate_path(G, path)

# Suorita ohjelma
if __name__ == "__main__":
    main()
