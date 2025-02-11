import graphviz
import logging
from collections import defaultdict

def identify_IDs(grid):
    """
    Identifies buildings, warehouses, and roads in a grid, and creates connections between them.
    
    Args:
        grid (list of list of str): A 2D grid with strings representing buildings, warehouses, roads, or empty spaces.
    
    Returns:
        tuple: (nodes, edges) where:
            - nodes is a dictionary with node coordinates and their types.
            - edges is a dictionary with connections between nodes.
    """
    nodes = {}
    edges = defaultdict(list) # Using a defaultdict to handle missing keys
    road_nodes = set()
    try: 
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                cell = grid[x][y]
                # Check if the cell is a building, warehouse or road
                if cell.startswith("B"):
                   nodes[(x,y)] = {"type": "Building", "id": cell}
                elif cell.startswith("W"):
                   nodes[(x,y)] = {"type": "Warehouse", "id": cell}
                elif cell.startswith("R"):
                   width = int(cell[1:])
                   nodes[(x,y)] = {"type": "Road", "width": width}
                   road_nodes.add((x,y))
                else:
                    nodes[(x,y)] = {"type": "Empty"}

        # Identify roads and connect them
        for (x,y) in road_nodes:
            # Check the neighboring roads
            neighbors = [(x+dx, y+dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
            connected_roads = [(n, nodes[n]["width"]) for n in neighbors if n in road_nodes]
            
            # Identify intersections
            if len(connected_roads) >2:
                nodes[(x,y)]["type"] = "Intersection"
            
            for neighbor, width in connected_roads:
                current_width = nodes[(x,y)]["width"]
            
                if current_width != width:
                    mid_node = (x + neighbor[0]) / 2, (y + neighbor[1]) / 2
                    nodes[mid_node] = {"type": "Transition", "width": width}

                    edges[(x,y)].append((mid_node, current_width))
                    edges[mid_node].append((neighbor, width))
                else:
                    edges[(x,y)].append((neighbor, width))

        # Connect building and warehouses to the roads
        for (x,y), node in nodes.items():
            if node["type"] in ["Building", "Warehouse"]:
                neighbors = [(x+dx, y+dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
                road_neighbors = [n for n in neighbors if n in road_nodes]
                if road_neighbors:
                    edges[(x,y)] = [(road_neighbors[0], nodes[road_neighbors[0]]["width"])]

        logging.info(f"Nodes: {nodes}, Edges: {edges}")
        return nodes, edges
    except Exception as e:
        logging.error(f"{str(e)} - identify_IDs function")
        return None, None


def make_graph(nodes, edges):
    """
    Creates and renders a visual graph of nodes and their connections using Graphviz.
    
    Args:
        nodes (dict): A dictionary of nodes with their coordinates and types.
        edges (dict): A dictionary of node connections and their weights.
    
    Generates:
        A PNG image of the road network with nodes and edges visualized.
    """
    dot = graphviz.Digraph(format='png')
    try:
        for (x, y), node in nodes.items():
            label = node.get("id", "")
            if node["type"] == "Building":
                dot.node(f"{x},{y}", label, shape='box', style='filled', fillcolor='blue')
            elif node["type"] == "Warehouse":
                dot.node(f"{x},{y}", label, shape='box', style='filled', fillcolor='red')
            elif node["type"] == "Intersection":
                dot.node(f"{x},{y}", shape='circle', style='filled', fillcolor='gray')
            elif node["type"] == "Transition":
                dot.node(f"{x},{y}", shape='diamond', style='filled', fillcolor='green')
        
        for node, connections in edges.items():
            for neighbor, weight in connections:
                dot.edge(f"{node[0]},{node[1]}", f"{neighbor[0]},{neighbor[1]}", label=str(weight))
        
        dot.render('road_network', view=True)
    except Exception as e:
        logging.error(str(e))