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
edges = [
    ("A", "B"),
    ("A", "C"),
    ("A", "D"),
    ("B", "A"),
    ("B", "E"),
    ("B", "C"),
    ("C", "A"),
    ("C", "B"),
    ("C", "D"),
    ("C", "F"),
    ("D", "A"),
    ("D", "C"),
    ("D", "G"),
    ("E", "B"),
    ("E", "F"),
    ("E", "H"),
    ("F", "C"),
    ("F", "E"),
    ("F", "G"),
    ("F", "I"),
    ("G", "D"),
    ("G", "F"),
    ("G", "J"),
    ("H", "E"),
    ("H", "I"),
    ("H", "K"),
    ("I", "F"),
    ("I", "H"),
    ("I", "J"),
    ("I", "L"),
    ("J", "G"),
    ("J", "I"),
    ("J", "M"),
    ("K", "H"),
    ("K", "L"),
    ("K", "N"),
    ("L", "I"),
    ("L", "K"),
    ("L", "M"),
    ("L", "N"),
    ("M", "J"),
    ("M", "L"),
    ("M", "N"),
    ("N", "K"),
    ("N", "L"),
    ("N", "M")
]

# Add edges with random weights
for edge in edges:
    weight = round(random.uniform(0, 1), 2) # Round to 2 sig figs
    G.add_edge(edge[0], edge[1], weight=weight)

# Rolling with a planar layout to minimize crossing edges and overlapping nodes
pos = nx.planar_layout(G)


@app.route("/")
def home():
    return render_template('index.html')

# To display the topology
@app.route('/display-topology')
def display_topology():
    
    edge_labels = {k: f"{v:.2f}" for k, v in nx.get_edge_attributes(G, "weight").items()} # 2 sig figs

    # draw graph
    plt.figure(figsize=(12,12))
        
    nx.draw_planar(G, with_labels=True,
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


@app.route('/dijkstra')
# Uses built-in dijkstra from networkx to find shortest path
def dijkstra():

    # Use global graph G to compute the shortest path
    source = "A"
    target = "N"
    try:
        # Set's shortest path using Dijkstra's algorithm
        shortest_path = nx.dijkstra_path(G, source=source, target=target, weight="weight")

        # Extract edges from the shortest path
        shortest_path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
    
        # Get edge weights for labeling
        edge_labels = nx.get_edge_attributes(G, "weight")
        filtered_edge_labels = {
            (min(edge), max(edge)): f"{edge_labels[(min(edge), max(edge))]:.2f}" # 2 sig figs
            for edge in shortest_path_edges
        }

        # Create subgraph for shortest path
        subgraph = nx.Graph()
        subgraph.add_nodes_from(shortest_path)
        subgraph.add_edges_from(shortest_path_edges)

        # Draw the shortest path graph
        plt.figure(figsize=(12, 12))

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