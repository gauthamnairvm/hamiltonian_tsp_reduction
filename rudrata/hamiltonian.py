import pandas as pd

def find_cycle(csv_path):

    rudrata_cycles = []
    def complete_graph(graph_data, alpha):
        # Copy of the input graph G
        G_prime = graph_data.copy()

        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                # Check if there exists an edge between two vertices i and j,
                # and assign edge weight as 1 + alpha if there are none.
                if graph_data.iloc[i, j] == 0:
                    G_prime.iloc[i, j] = 1 + alpha
                    G_prime.iloc[j, i] = 1 + alpha

        return G_prime

    #Function to find tours using backtracking
    def find_tours(graph, v, currPos, n, count, cost, path, start_node):
        if (count == n and graph.iloc[currPos,start_node]==1):
            if cost + graph.iloc[currPos,start_node] == n:
                rudrata_cycles.append(path + [start_node])  # Add the starting node to complete the cycle
                return True  # Cycle found, return True
            return False

        # BACKTRACKING STEP
        # Loop to traverse the adjacency matrix
        # of currPos node and increasing the count
        # by 1 and cost by graph[currPos][i] value
        for i in range(n):
            if (v[i] == False and graph.iloc[currPos,i]==1):
                
                # Mark as visited
                v[i] = True
                if find_tours(graph, v, i, n, count + 1, 
                    cost + graph.iloc[currPos,i], path + [i], start_node):
                    return True  # Return True if a cycle is found
                
                # Mark ith node as unvisited
                v[i] = False
        return False

    # Graph Data is stored as a matrix in a csv file, where the size of the matrix is V x V.
    G = pd.read_csv(csv_path)  # Dataframe to store the input matrix representation of a graph G
    node_ids = G.columns
    num_vertices = len(G)

    #Create a complete graph G' along with the existing edges in G.
    G_prime = complete_graph(G, num_vertices)

    #for start_vertex in range(num_vertices):
    visited = [False] * num_vertices
    visited[0] = True

    if find_tours(G_prime, visited, 0, num_vertices, 1, 0, [0],0):
        return G, G_prime, node_ids, rudrata_cycles[0]
        
    return G, G_prime, node_ids, []
    