from flask import Flask, jsonify, render_template, request, send_from_directory
import json
import pandas as pd
import csv
import os
import hamiltonian
import graph_visualization


app = Flask(__name__)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(message='Please choose a file.', success=False), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(message='No file selected', success=False), 400
    
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join('../rudrata/datasets', 'grid_data.csv')

        try:
            file.save(filepath)
            file_checkdf = pd.read_csv(filepath)
            header_row = file_checkdf.columns
            # Check for row_count
            if file_checkdf.shape[0]!= len(header_row) or file_checkdf.shape[1] != len(header_row):
                return jsonify(message='CSV file does not have NxN dimensions. (N= number of vertices)', success=False), 400
            
            # Check for self edges (diagonal elements should be 0)
            for i in range(len(header_row)):
                if file_checkdf.iloc[i, i] != 0:
                    return jsonify(message='Self edges should be 0 in the CSV file', success=False), 400
                    
            # Check if all values are 0's or 1's
            if not ((file_checkdf.values == 0) | (file_checkdf.values == 1)).all():
                return jsonify(message='Please provide an unweighted graph. Matrix should only contain 0s and 1s', success=False), 400
                    
            return jsonify(message='File successfully uploaded and processed', success=True), 200
        
        except Exception as e:
            return jsonify(message='Error processing uploaded file', success=False), 500
        
    else:
        return jsonify(message='Invalid file format. Only CSV files are accepted.', success=False), 400


@app.route('/process_grid', methods=['POST'])
def process_grid():
    grid_data = request.json  # Get the JSON data sent from the client

    # Extract the size of the grid
    size = 0
    for pair in grid_data:
        for val in pair:
            if val > size:
                size = val

    # Create a matrix of size s x s filled with zeros
    grid_matrix = [[0] * size for _ in range(size)]

    # Set grid elements to 1 based on received indices
    for pair in grid_data:
        i, j = pair
        grid_matrix[i-1][j-1] = 1  # Adjust indices to 0-based

    # Write the grid matrix to a CSV file
    with open('../rudrata/datasets/grid_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list(range(1,size+1)))
        writer.writerows(grid_matrix)
    return "Data received"

@app.route('/redirect_rudrataviz', methods=['GET'])
def redirect_rudrataviz():
    input_graphdf, converted_graphdf, node_ids,rudrata_cycles = hamiltonian.find_cycle("../rudrata/datasets/grid_data.csv")
    input_json = graph_visualization.visualize_graph(input_graphdf, 'rudrata_input',[])
    input_json_file = '../rudrata/datasets/rudrata_input.json'
    with open(input_json_file, 'w') as file:
        json.dump(input_json, file, indent=4)
    converted_json = graph_visualization.visualize_graph(converted_graphdf, 'complete_graph',[])
    converted_json_file = '../rudrata/datasets/complete_graph.json'
    with open(converted_json_file, 'w') as file:
        json.dump(converted_json, file, indent=4)
    show_alert = False
    if len(rudrata_cycles)==0:
        # If no cycles are found, set a flag to show the alert
        show_alert = True
        print("There are no `RUDRATA CYCLES` in graph G")
    else:
        print("The following cycles were found \n",rudrata_cycles)

        rudrata_output_json = graph_visualization.visualize_graph(input_graphdf, 'rudrata_output',rudrata_cycles)
        rudrata_json_file = '../rudrata/datasets/rudrata_output.json'
        with open(rudrata_json_file, 'w') as file:
            json.dump(rudrata_output_json, file, indent=4)
        
        tsp_output_json = graph_visualization.visualize_graph(converted_graphdf, 'tsp_output', rudrata_cycles)
        tsp_json_file = '../rudrata/datasets/tsp_output.json'
        with open(tsp_json_file, 'w') as file:
            json.dump(tsp_output_json, file, indent=4)
        
    return render_template('rudrataviz.html', show_alert=show_alert, cycle=[input_graphdf.columns[i] for i in rudrata_cycles])

@app.route('/')
def homepage():
    return render_template('initial.html',show_alert=True)

@app.route('/datasets/rudrata_input.json')
def serve_rudrata_input():
    return send_from_directory('../rudrata/datasets','rudrata_input.json')
@app.route('/datasets/complete_graph.json')
def serve_complete_graph():
    return send_from_directory('../rudrata/datasets', 'complete_graph.json')

@app.route('/datasets/rudrata_output.json')
def serve_rudrata_output():
    return send_from_directory('../rudrata/datasets', 'rudrata_output.json')

@app.route('/datasets/tsp_output.json')
def serve_tsp_input():
    return send_from_directory('../rudrata/datasets', 'tsp_output.json')

app.route('/static/sample.png')
def serve_sample_image():
    return send_from_directory('../rudrata/static', 'sample.png')

if __name__ == '__main__':
    app.run(debug=True)
