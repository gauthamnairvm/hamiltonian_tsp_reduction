### Transformation from RUDRATA/HAMILTONIAN to TSP

## Input Format

A CSV file consists of a first row of node names (vertex IDs) followed by an adjacency matrix representing the undirected edges. The matrix should be an N times N matrix where N is the number of nodes contained in the graph. This adjacency matrix would consist of either a 1 or a 0 at a particular index where 1 implies an existing edge and 0 implies none. The provided edges should be undirected and self edges should be set to 0. The minimum number of vertices to be provided is at least 3 and the maximum vertices should not exceed 16.

Sample valid and invalid csv input formats can be found in the test_graphs/ directory.

Alternatively users can use a clickable grid matrix that creates the csv file with numbered vertices as the file header.


## Transformation

The transformation algorithm from RUDRATA to TSP involves creating a complete weighted undirected graph G' from the given input graph G. Existing edges are assigned a weight of 1, and missing edges are added with a weight of 1 + alpha, where alpha is the number of vertices in G.

### Construction of G'

- **Graph Completion**: Adds missing edges with weight 1 + alpha to make the input graph complete.
- **Edge Weight Adjustment**: Maintains existing edges with a weight of 1.

### Finding a Tour in G'

- **Backtracking Algorithm**: A simple backtracking algorithm is used to find tours within a specified budget (number of vertices in G).
- **Tour Verification**: Checks if a tour can be completed within the budget without using any added edges.

The python script rudrata\hamiltonian_visualization.py transforms the input graph csv file present at the given file path to a complete graph and employs logic to detect the existance of a rudrata/hamiltonian cycle.

### Visualizing the graphs
The python script rudrata\graph_visualization.py contains the logic to convert pandas dataframe objects to valid json format. The json files are then visualized using [3D Force-Directed Graph repository](https://github.com/vasturiano/3d-force-graph)

## Setup

Clone the repository to your local machine and run the following commands,

<!-- For Windows cmd prompt -->
```bash
#Install Flask and other dependencies
pip install Flask
# Change to the appropriate directory
cd rudrata

# Start the Flask application
python app.py
```

## Requirements and Dependencies

- **BROWSER - Microsoft Edge(Version 123.0.+)**
- **Python 3.11**
- **JavaScript ES 6**
- **Pandas 1.5.3**
- **Flask 2.2.2**

The HTML rudrata\templates\initial.html contains a template to the homepage that accepts user input, and rudrata\templates\rudrataviz.html contains a template to visualize the transformations. These templates can be manipulated to edit the webapp elements as per the requirement/preference. 