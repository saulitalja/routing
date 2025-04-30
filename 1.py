import networkx as nx
import matplotlib.pyplot as plt
import heapq

def dijkstra(graph, source):
    dist = {node: float('inf') for node in graph.nodes()}
    prev = {node: None for node in graph.nodes()}
    dist[source] = 0
    queue = [(0, source)]

    while queue:
        current_dist, u = heapq.heappop(queue)

        if current_dist > dist[u]:
            continue

        for v in graph.neighbors(u):
            weight = graph[u][v]['weight']
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                prev[v] = u
                heapq.heappush(queue, (dist[v], v))

    return dist, prev

def reconstruct_path(prev, target):
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    return path[::-1]

def print_and_save_routing_tables(graph, filename="reititystaulut.txt"):
    with open(filename, 'w') as f:
        for router in graph.nodes():
            dist, prev = dijkstra(graph, router)
            header = f"Reititystaulu reitittimelle {router}:\n"
            print(header, end='')
            f.write(header)
            for target in graph.nodes():
                if target == router:
                    continue
                if dist[target] == float('inf'):
                    line = f" -> Reititin {target}: ei reittiä\n"
                else:
                    path = reconstruct_path(prev, target)
                    path_str = " -> ".join(map(str, path))
                    line = f" -> Reititin {target}: etäisyys {dist[target]}, reitti: {path_str}\n"
                print(line, end='')
                f.write(line)
            print()
            f.write("\n")

def draw_network(graph):
    pos = nx.spring_layout(graph, seed=42)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=1200, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.title("OSPF-verkko")
    plt.show()

def main():
    G = nx.Graph()

    num_routers = int(input("Syötä reitittimien määrä: "))
    G.add_nodes_from(range(num_routers))

    num_links = int(input("Syötä reittien määrä: "))
    for i in range(num_links):
        print(f"Linkki {i+1}:")
        u = int(input("  Alku (reititin): "))
        v = int(input("  Loppu (reititin): "))
        w = int(input("  Paino (etäisyys): "))
        G.add_edge(u, v, weight=w)

    print("\nSuoritetaan OSPF (Dijkstra) jokaiselle reitittimelle...\n")
    print_and_save_routing_tables(G)

    print("\nPiirretään verkko graafisesti...")
    draw_network(G)

if __name__ == "__main__":
    main()
