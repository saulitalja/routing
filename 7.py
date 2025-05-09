import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def read_network_from_file(filename="reittitiedosto.txt"):
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

def build_graph_and_paths(num_nodes, links):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for u, v, w in links:
        G.add_edge(u, v, weight=w)

    routing_paths = {}
    for src in range(num_nodes):
        try:
            _, paths = nx.single_source_dijkstra(G, src)
            routing_paths[src] = paths
        except nx.NetworkXNoPath:
            routing_paths[src] = {}
    return G, routing_paths

def shortest_path(start, end, routing_paths):
    if start in routing_paths and end in routing_paths[start]:
        return routing_paths[start][end]
    else:
        print("❌ Reittiä ei löytynyt.")
        return []

def animate_path(G, path):
    #pos = nx.spring_layout(G, seed=42)
    pos = nx.spring_layout(G, seed=42, k=1.0, iterations=200)
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
    total_distance = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        total_distance += G[u][v]['weight']
    # Lasketaan kokonaisetäisyys ja muodostetaan välivaiheiden laskulauseke
    distance_parts = []
    total_distance = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        w = G[u][v]['weight']
        distance_parts.append(str(w))
        total_distance += w

    expression = " + ".join(distance_parts) + f" = {total_distance}"

    plt.title(f"Paketin reitti: {path}\nEtäisyys: {expression}")

    #plt.title(f"Paketin reitti: {path} (etäisyys: {total_distance})")
    #plt.title(f"Paketin reitti: {path}")
    plt.show()

def prompt_modify_network(num_nodes, links):
    while True:
        print("\n🔧 Valinnat: [L]isää node, [P]oista node, [J]atka, [Q]uit")
        choice = input("Valintasi: ").strip().lower()

        if choice == 'l':
            new_node = num_nodes
            num_nodes += 1
            print(f"✅ Lisätty solmu {new_node}. Lisää siihen yhteyksiä (tyhjä lopettaa):")
            while True:
                conn = input(f"Yhteys muodossa <kohde> <etäisyys>: ").strip()
                if not conn:
                    break
                try:
                    target, weight = map(int, conn.split())
                    if 0 <= target < num_nodes - 1 and weight > 0:
                        links.append((new_node, target, weight))
                        print(f" - Lisätty yhteys {new_node} <--> {target} (etäisyys {weight})")
                    else:
                        print("❌ Virheellinen kohde tai etäisyys.")
                except:
                    print("❌ Anna arvot muodossa: numero numero")
        elif choice == 'p':
            try:
                rem = int(input(f"Anna poistettavan solmun numero (0 - {num_nodes-1}): "))
                if 0 <= rem < num_nodes:
                    links[:] = [(u, v, w) for u, v, w in links if u != rem and v != rem]
                    # Päivitetään node-indeksit — ei tehdä reindexointia, vaan pidetään "aukko"
                    print(f"✅ Poistettu solmu {rem} ja siihen liittyvät yhteydet.")
                else:
                    print("❌ Solmua ei ole.")
            except:
                print("❌ Anna numeroarvo.")
        elif choice == 'j':
            return num_nodes, links
        elif choice == 'q':
            exit()
        else:
            print("❌ Tuntematon valinta.")

def main():
    if not os.path.exists("reittitiedosto.txt"):
        print("❌ Tiedostoa 'reittitiedosto.txt' ei löytynyt.")
        return

    num_nodes, links = read_network_from_file("reittitiedosto.txt")

    while True:
        G, routing_paths = build_graph_and_paths(num_nodes, links)

        print("\n✅ Verkon rakenne:")
        for u, v, w in links:
            print(f" - {u} <--> {v} (etäisyys {w})")

        try:
            start = int(input("\nAnna lähdesolmu: "))
            end = int(input("Anna kohdesolmu: "))
            if not (0 <= start < num_nodes and 0 <= end < num_nodes):
                raise ValueError()
        except ValueError:
            print("❌ Virheellinen solmun numero.")
            continue

        path = shortest_path(start, end, routing_paths)
        #if path:
        #    print(f"✅ Laskettiin reitti: {path}")
        #    animate_path(G, path)
        #if path:
        # Laske kokonaisetäisyys reitin varrelta
            #total_distance = 0
            #for i in range(len(path) - 1):
            #    u, v = path[i], path[i+1]
            #    total_distance += G[u][v]['weight']
            #print(f"✅ Laskettiin reitti: {path} (kokonaisetäisyys: {total_distance})")
            #animate_path(G, path)
        if path:
        # Laske etäisyys ja muodosta laskulauseke
            distance_parts = []
            total_distance = 0
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                w = G[u][v]['weight']
                distance_parts.append(str(w))
                total_distance += w
            expression = " + ".join(distance_parts) + f" = {total_distance}"

            print(f"✅ Laskettiin reitti: {path} (etäisyys: {expression})")
            animate_path(G, path)


        num_nodes, links = prompt_modify_network(num_nodes, links)

if __name__ == "__main__":
    main()
