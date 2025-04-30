import networkx as nx
import matplotlib.pyplot as plt
import os

def initialize_routing_tables(num_routers, links):
    tables = []
    for i in range(num_routers):
        table = {}
        for j in range(num_routers):
            if i == j:
                table[j] = (0, j)
            else:
                table[j] = (float('inf'), None)
        tables.append(table)

    for u, v, cost in links:
        tables[u][v] = (cost, v)
        tables[v][u] = (cost, u)

    return tables

def update_routing_table(tables, current, neighbor, cost_to_neighbor):
    updated = False
    for dest in range(len(tables)):
        if dest == current:
            continue
        neighbor_cost, _ = tables[neighbor][dest]
        if neighbor_cost + cost_to_neighbor < tables[current][dest][0]:
            tables[current][dest] = (neighbor_cost + cost_to_neighbor, neighbor)
            updated = True
    return updated

def rip_simulation(num_routers, links):
    tables = initialize_routing_tables(num_routers, links)
    neighbors = [[] for _ in range(num_routers)]
    for u, v, _ in links:
        neighbors[u].append(v)
        neighbors[v].append(u)

    changes = True
    round = 0
    while changes:
        changes = False
        round += 1
        print(f"\n--- RIP-kierros {round} ---")
        for router in range(num_routers):
            for neighbor in neighbors[router]:
                cost_to_neighbor = tables[router][neighbor][0]
                if update_routing_table(tables, router, neighbor, cost_to_neighbor):
                    changes = True
    return tables

def print_routing_tables(tables):
    for i, table in enumerate(tables):
        print(f"\nReititystaulu reitittimelle {i}:")
        for dest, (cost, next_hop) in table.items():
            if cost == float('inf'):
                print(f" -> {dest}: ei reittiä")
            else:
                print(f" -> {dest}: etäisyys {cost}, seuraava {next_hop}")

def save_to_file(tables, filename="rip_reititystaulut.txt"):
    with open(filename, 'w') as f:
        for i, table in enumerate(tables):
            f.write(f"Reititystaulu reitittimelle {i}:\n")
            for dest, (cost, next_hop) in table.items():
                if cost == float('inf'):
                    f.write(f" -> {dest}: ei reittiä\n")
                else:
                    f.write(f" -> {dest}: etäisyys {cost}, seuraava {next_hop}\n")
            f.write("\n")

def draw_network(num_routers, links):
    G = nx.Graph()
    G.add_nodes_from(range(num_routers))
    for u, v, cost in links:
        G.add_edge(u, v, weight=cost)

    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("RIP-reititysverkko")
    plt.show()

def read_network_from_file(filename):
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

def ask_network_input():
    num_routers = int(input("Syötä reitittimien määrä: "))
    num_links = int(input("Syötä reittien määrä: "))
    links = set()

    for i in range(num_links):
        print(f"Linkki {i+1}:")
        while True:
            u = int(input("  Alku (reititin): "))
            v = int(input("  Loppu (reititin): "))
            if u == v:
                print("  ❌ Et voi yhdistää reititintä itseensä.")
                continue
            if not (0 <= u < num_routers and 0 <= v < num_routers):
                print(f"  ❌ Reitittimien numerot oltava välillä 0–{num_routers - 1}")
                continue
            if (u, v) in links or (v, u) in links:
                print("  ❌ Yhteys on jo määritelty.")
                continue
            cost = int(input("  Paino (etäisyys, vähintään 1): "))
            if cost <= 0:
                print("  ❌ Etäisyyden on oltava positiivinen kokonaisluku.")
                continue
            break
        links.add((u, v, cost))

    return num_routers, list(links)

def main():
    print("Haluatko lukea verkon tiedostosta (verkko.txt)? (k/e): ", end='')
    from_file = input().strip().lower() == 'k'
    if from_file and os.path.exists("verkko.txt"):
        num_routers, links = read_network_from_file("verkko.txt")
        print(f"\n✅ Luettiin {len(links)} linkkiä tiedostosta.")
    else:
        num_routers, links = ask_network_input()

    print("\n--- Suoritetaan RIP ---")
    tables = rip_simulation(num_routers, links)

    print("\n--- LOPULLISET REITITYSTAULUT ---")
    print_routing_tables(tables)

    save_to_file(tables)
    print("\n💾 Reititystaulut tallennettu tiedostoon: rip_reititystaulut.txt")

    draw_network(num_routers, links)

if __name__ == "__main__":
    main()
