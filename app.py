import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import io
import os
import signal
import random
from flask import Flask, render_template, Response, request

# initialize Flask
app = Flask (__name__)

# Global graph
G = nx.Graph()

# Global nodes & edges
# NOV 21 @2127 trying out a smaller graph goings from A to H
edges = [
    ("A", "B"),
    ("A", "C"),
    ("A", "D"),
    ("B", "A"),
    ("B", "C"),
    ("B", "E"),
    ("C", "A"),
    ("C", "B"),
    ("C", "F"),
    ("C", "D"),
    ("D", "A"),
    ("D", "C"),
    ("D", "G"),
    ("E", "B"),
    ("E", "F"),
    ("E", "H"),
    ("F", "C"),
    ("F", "E"),
    ("F", "H"),
    ("F", "G"),
    ("G", "F"),
    ("G", "D"),
    ("G", "H"),
    ("H", "E"),
    ("H", "F"),
    ("H", "G"),
]

# Nodes in position of a diamond shape topology
pos = {
    "A": (-2, 0),
    "B": (1, 2),
    "C": (1, 0),
    "D": (1, -2),
    "E": (3, 2),
    "F": (3, 0),
    "G": (3, -2),
    "H": (6, 0),
}

# Add edges with random weights
for edge in edges:
    weight = round(random.uniform(0, 1), 2) # Round to 2 sig figs
    G.add_edge(edge[0], edge[1], weight=weight)

@app.route("/")
def home():
    return render_template('index.html')

# To display the topology
@app.route('/display-topology')
def display_topology():
    
    edge_labels = {k: f"{v:.2f}" for k, v in nx.get_edge_attributes(G, "weight").items()} # 2 sig figs

    # draw graph
    plt.figure(figsize=(12,12))

    # Originally was drawn as planar, trying out different combos
    nx.draw(G,
            pos, # added position of nodes 
            with_labels=True,
            node_color="blue", 
            node_size=2000,
            font_size=10, 
            font_color="white",
            edge_color="gray")
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                 font_size=10, label_pos=0.5)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(0)

    return Response(img.getvalue(), mimetype='image/png')

# Remove node function
@app.route('/kill-node', methods=['GET'])
def kill_node():
    node = request.args.get('node')
    print(f"Received node to remove: {node}")

    # Check for specified node
    if not node:
        return "No node specified. Please provide a valid node to remove.", 400
    
    # Check if specified node is on graph
    if node not in G.nodes:
        return f"Node '{node}' does not exist in the graph.", 404
    
    # Remove specified node that is on the graph
    G.remove_node(node)
    print(f"Node {node} and its edges have been removed.")

    edge_labels = {k: f"{v:.2f}" for k, v in nx.get_edge_attributes(G, "weight").items()}

    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True,
            node_color="blue",
            node_size=2000,
            font_size=10,
            font_color="white",
            edge_color="gray")
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=10,
                                 label_pos=0.5)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return Response(img.getvalue(), mimetype='image/png')

# Remove edge function
@app.route('/edge-removal', methods=['GET'])
def remove_edge():
    node1 = request.args.get('node_1')
    node2 = request.args.get('node_2')
    print(f"Received edge to remove: {node1} to {node2}")

    # Check for valid nodes
    if not node1 or not node2:
        return "Both nodes of the edge must be specified. Please provide valid nodes.", 400
    
    # Check if valid nodes have a shared edge
    if not G.has_edge(node1, node2):
        return f"The edge from '{node1} to {node2} does not exist in the graph.", 404
    
    # Removes valid nodes & output to terminal the designated edge
    G.remove_edge(node1, node2)
    print(f"Edge from {node1} to {node2} has been removed.")

    edge_labels = {k: f"{v:.2f}" for k, v in nx.get_edge_attributes(G, "weight").items()}

    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True,
            node_color="blue",
            node_size=2000,
            font_size=10,
            font_color="white",
            edge_color="gray")
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=10,
                                 label_pos=0.5)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return Response(img.getvalue(), mimetype='image/png')

@app.route('/dijkstra')
# Uses built-in dijkstra from networkx to find shortest path
def dijkstra():
    # Use global graph G to compute the shortest path
    source = "A"
    # note --> Decreasing the graph size to minimize overlapping edge labels/nodes and crossing edges -- target = "N"
    target = "H"
    try:
        # Set's shortest path using Dijkstra's algorithm
        shortest_path = nx.dijkstra_path(G, source=source, target=target, weight="weight")

        # Extract edges from the shortest path
        shortest_path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
    
        # Get edge weights for labeling
        edge_labels = nx.get_edge_attributes(G, "weight")
        filtered_edge_labels = {
            
            #(min(edge), max(edge)): f"{edge_labels[(min(edge), max(edge))]:.2f}" # 2 sig figs
            #for edge in shortest_path_edges
            
            edge: f"{edge_labels.get(edge, edge_labels.get((edge[1], edge[0]), 0)):.2f}" for edge in shortest_path_edges
        }

        # Create subgraph for shortest path
        subgraph = nx.Graph()
        subgraph.add_nodes_from(shortest_path)
        subgraph.add_edges_from(shortest_path_edges)

        # Draw the shortest path graph
        plt.figure(figsize=(12, 12))

        # Shortest path graph will display the nodes in green and edges in red
        nx.draw(subgraph, pos, with_labels=True,
                node_color="green",
                edge_color="red",
                node_size=2000,
                font_size=10,
                font_color="white")
        
        nx.draw_networkx_edge_labels(subgraph, pos, 
                                     edge_labels=filtered_edge_labels, 
                                     font_size=10,
                                     label_pos=0.5)
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return Response(img.getvalue(), mimetype='image/png')
    except nx.NetworkXNoPath:
        return "No path exists between {} and {}".format(source, target), 404
    
@app.route('/exit')
# Close program
def exit():
    try:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            os._exit(0)
        func()
        return "Server shutting down..."
    except Exception as e:
        return f"Error shutting down server: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)