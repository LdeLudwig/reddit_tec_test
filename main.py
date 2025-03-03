import logging
from graph_maker import identify_IDs, make_graph

# Initialize logging
logging.basicConfig(filename='./log/graph_maker.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define your grid here
grid=[
        ["B1", "W1", "R2", "R2", "R1"],
        ["R1", "R1", "R2", "R1", "0"],
        ["R1", "R2", "R1", "B2", "R1"],
        ["R2", "W2", "R1", "B2", "B2"],
        ["B3", "B3", "0", "R1", "0"]
    ]

def main(grid):
    """
    Processes the grid to identify nodes and edges, then generates a graph visualization.
    
    Args:
        grid (list of list of str): A 2D grid representing buildings, warehouses, roads, and empty spaces.
    
    Logs:
        Errors if nodes or edges cannot be identified.
    """
    nodes, edges = identify_IDs(grid)
    if nodes and edges:
        make_graph(nodes, edges)
    else:
        logging.error("Failed to identify nodes or edges.")

if __name__ == "__main__":
    main(grid)