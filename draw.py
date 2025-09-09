import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
G.add_nodes_from(["a", "b", "c", "d", "e"])
G.add_edges_from([
    ("a", "b"), ("a", "c"), ("a", "d"),
    ("b", "e"), ("b", "d"),
    ("e", "d"), ("c", "d")
])


pos = {
    "a": (-1.4, 0.2),    
    "b": (0.2, -1.0),    
    "c": (0.2, 1.2),     
    "d": (1.6, 0.2),     
    "e": (-1.4, -1.4)    
}


plt.figure(figsize=(5, 4))
nx.draw(
    G, pos,
    with_labels=True,
    labels={n: n for n in G.nodes()},
    node_size=900,
    node_color="white",
    edge_color="black",
    font_size=14,
    width=2,
    font_weight="regular"
)
plt.axis("off")
plt.tight_layout()
plt.savefig("graph_i_final.png", dpi=300)
plt.show()

