import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

#Remove the three lines of code below to get rid of the fixed nodes' position and their edges
seed=0
random.seed(0)
np.random.seed(0)

G = nx.Graph()

# Add nodes and provide label names
G.add_node("A")
G.add_node("B")
G.add_node("C")
G.add_node("D")
G.add_node("E")
G.add_node("F")

# Add edges from first node to the next one
G.add_edge("A", "C")
G.add_edge("B", "C")
G.add_edge("B", "D")
G.add_edge("C", "E")
G.add_edge("D", "C")
G.add_edge("D", "E")
G.add_edge("E", "F")

# Properties of styling the nodes and edges
nx.draw(G, with_labels=True, node_color="blue", node_size=3000, font_color="white", 
font_weight="bold", font_size="20", font_family="Times New Roman", width=5)

plt.margins(0.2)
plt.show()