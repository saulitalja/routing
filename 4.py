import random
import time
import networkx as nx
import matplotlib.pyplot as plt

class BGPRouter:
    def __init__(self, operator_name, as_number):
        self.operator_name = operator_name  # Käytetään operaattorin nimeä AS:n sijasta
        self.as_number = as_number  # AS-numero
        self.routing_table = {}
        self.peers = []

    def add_peer(self, peer):
        """Lisää BGP-naapuri (peer)."""
        self.peers.append(peer)

    def send_update(self):
        """Lähetä reitityspäivitys naapureille."""
        for peer in self.peers:
            peer.receive_update(self.routing_table, self.operator_name)

    def receive_update(self, routes, peer_operator):
        """Vastaanota reitityspäivitys naapureilta."""
        print(f"{self.operator_name} vastaanotti reitityspäivityksen {peer_operator}:ltä")
        
        for prefix, cost in routes.items():
            if prefix not in self.routing_table or self.routing_table[prefix] > cost:
                self.routing_table[prefix] = cost
                print(f"{self.operator_name} päivitti reitin {prefix}: etäisyys {cost}")

    def display_routing_table(self):
        """Näytä reititystaulu."""
        print(f"{self.operator_name} ({self.as_number}) Reititystaulu:")
        for prefix, cost in self.routing_table.items():
            print(f"  {prefix} => Etäisyys: {cost}")

    def get_routing_data(self):
        """Hae reititystiedot kaaviota varten."""
        return [(self.operator_name, prefix, cost) for prefix, cost in self.routing_table.items()]

def bgp_simulation():
    # Luo kolme BGP-reititintä (Elisa, Telia, DNA)
    elisa = BGPRouter("Elisa", 16086)
    telia = BGPRouter("Telia", 1299)
    dna = BGPRouter("DNA", 16083)

    # Liitä reitittimet naapureiksi
    elisa.add_peer(telia)
    telia.add_peer(elisa)
    telia.add_peer(dna)
    dna.add_peer(telia)

    # Määrittele alkuperäiset reitit BGP-reitittimille
    elisa.routing_table = {'10.0.0.0/24': 10, '192.168.1.0/24': 20}
    telia.routing_table = {'10.0.0.0/24': 5, '192.168.1.0/24': 15}
    dna.routing_table = {'10.0.0.0/24': 15, '192.168.1.0/24': 10}

    # Lähetä alkuperäiset reitityspäivitykset
    print("\nAlustavat reititystaulut:")
    elisa.display_routing_table()
    telia.display_routing_table()
    dna.display_routing_table()

    # Simuloi reitityspäivitykset
    print("\nReitityspäivitykset käynnissä...\n")
    for _ in range(3):
        time.sleep(2)  # Odotetaan vähän, jotta päivitykset näkyvät
        elisa.send_update()
        telia.send_update()
        dna.send_update()

    # Näytä päivittyneet reititystaulut
    print("\nPäivittyneet reititystaulut:")
    elisa.display_routing_table()
    telia.display_routing_table()
    dna.display_routing_table()

    # Visualisoi verkko
    visualize_bgp([elisa, telia, dna])

def visualize_bgp(routers):
    """Visualisoi BGP-verkko ja reititystiedot."""
    G = nx.Graph()

    label_map = {}

    # Lisää solmut ja linkit
    for router in routers:
        node_label = f"{router.operator_name}\nAS{router.as_number}"
        G.add_node(node_label)
        label_map[router.operator_name] = node_label

    for router in routers:
        for peer in router.peers:
            G.add_edge(label_map[router.operator_name], label_map[peer.operator_name])

    # Luo kaavio
    pos = nx.spring_layout(G, seed=42)  # Aseta solmujen asettelu
    plt.figure(figsize=(8, 6))

    # Piirrä verkko
    nx.draw(G, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=3000,
            font_weight='bold',
            font_size=10,
            font_color='black')

    plt.title("BGP Reititysverkko - Elisa, Telia, DNA")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    bgp_simulation()
