from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
import networkx as nx
import io

app = Flask (__name__)

@app.route("/")
def home():
    return render_template('index.html')

# To display the topology
@app.route('/display-topology')
def display_topology():
    G = nx.Graph()
    G.add_edges_from([
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
    ])

    # #draw graph
    plt.figure(figsize=(12,12))
    plt.margins(0.2)
    
    nx.draw(G, with_labels=True, 
            node_color="blue", 
            node_size=2000,
            font_size=10, 
            font_color="white")
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(0)

    return Response(img.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)