# Road Network Graph Generator

## Description
This project generates a graphical representation of a road network based on a given grid. The grid consistes of buildings, warehouses, roads and empty spaces,
which are processed to identify nodes and edges. THe output is a visual representation using Graphviz.

## Installation
### Prerequisites
Ensure you have Python3 installed. Additionally, install the required dependencies:

```bash
    pip install -r requirements.txt
```
## Setting up the project
1. Clone the repository;
2. Install the required dependencies;
3. Run the main script:

## Usage
### Running the script
To execute the script, simply run:
```bash
    python main.py
```
THe script processes a predefined grid, identifies the nodes and edges, and
generates a graphical representation of the road network.

### Customizing the grid
You can modify the ```grid``` variable in ```main.py``` to represent your own grid.

### Output
 - The generated graph is saved as road_network.png.
 - Logs are stored in ```./log/graph_maker.log```

## Dependencies
 - Python 3.x
 - Graphviz
 - Logging (built-in Python module)

## License
This project is open-source and available under the MIT License.

## Author
Lucas Xavier