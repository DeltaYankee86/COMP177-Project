import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

def draw():
    #Remove the three lines of code below to get rid of the fixed nodes' position and their edges
    seed=0
    random.seed(0)
    np.random.seed(0)

    G = nx.Graph()

    # Adds nodes through a list
    # Additional info can be added to give the node more attributes
    # To add attrib, a {} give some the attrib a name and a value, add more if needed
    G.add_nodes_from(["A", "B", "C", "D", "E", "F"])

    # Generate positions using networkx layout function
    #positions = nx.spring_layout(G, seed=seed)


    # 11-12-2024 @2142 - Commented out to test out the various drawing functions of networkx
    # Manually inputting positions of the code
    positions = {
        "A": (-3, 2),
        "B": (1, 5),
        "C": (1, 1),
        "D": (3, 5),
        "E": (3, 0),
        "F": (4, -2)
    }


    ''' Note: Below is the means to hard code & add a node manually
    # Add nodes and provide label names
    G.add_node("A")
    G.add_node("B")
    G.add_node("C")
    G.add_node("D")
    G.add_node("E")
    G.add_node("F")
    '''


    ''' Note: Below is the means to hard code & add an edge manually
    # Add edges from first node to the next one
    G.add_edge("A", "C")
    G.add_edge("B", "C")
    G.add_edge("B", "D")
    G.add_edge("C", "E")
    G.add_edge("D", "C")
    G.add_edge("D", "E")
    G.add_edge("E", "F")
    '''

    # This sets the edges and provides additional
    # attrib that are associated with the link,
    # in this instance the cost of the link from one node to another.
    # The attrib can be called whatever you want.
    G.add_edges_from([
        ("A", "C", {"cost_of_link": 0.2}),
        ("B", "C", {"cost_of_link": 0.5}),
        ("B", "D", {"cost_of_link": 0.4}),
        ("C", "E", {"cost_of_link": 0.7}),
        ("D", "C", {"cost_of_link": 0.6}),
        ("D", "E", {"cost_of_link": 0.9}),
        ("E", "F", {"cost_of_link": 0.1}),
    ])

    edge_labels={(u,v): d["cost_of_link"] for u, v, d in G.edges(data=True)}

    # Properties of styling the nodes and edges
    # 11-12-2024 @ 2143 - removed attribute 'pos=positions'
    # @ 2143 - going to test out different graph drawings
    # various graph drawings: .draw, .draw_random, .draw_circular, .draw_shell, .draw_planar, .draw_spring
    nx.draw_spring(G, with_labels=True, node_color="blue", 
            node_size=3000, font_color="white", font_weight="bold",
            font_size="20", font_family="Times New Roman", 
            edge_color="lightgray", width=5)

    # Draws the labels/attributes for the edges
    # # 11-12-2024 @ 2143 - removed attribute 'pos=positions'
    nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=edge_labels, label_pos = 0.5)

    # networkx built-in function to output shortest path
    # call graph name, then from node to node
    print(nx.shortest_path(G, "A", "F"))

    plt.margins(0.2)
    plt.show()

    # Refer to 'Algorithm' in NetworkX documentation for Dijkstra’s algorithm to find the shortest weighted path

def dijkstra():
    print("I'll eventually put dijkstra in this def")


def main():
    print("\nWelcome dynamic routing design in faulty network. Please selection from the following options:")
    over = False
    while over is False:
        try:
            selection = int(input("\n [0] - Draw graph with labels\n [1] - See shortest path\n [2] - EXIT\n"))
            # Draw the topology
            if selection == 0:
                draw()
            # Output the Dijkstra's algorithm of the shortest path from starting node to destination node
            if selection == 1:
                dijkstra()
            # Exit
            if selection == 2:
                print(" GOODBYE ")
                over = True
        # Any invalid well result in staying in the menu
        except ValueError:
            print("Invalid input. Please center a valid selection.")
            

if __name__ == "__main__":
    main()