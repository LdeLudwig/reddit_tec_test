import graphviz
import logging
from collections import defaultdict

# Initialize logging
logging.basicConfig(filename='./log/graph_maker.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def identify_IDs(grid):
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
                   nodes[(x,y)] = {"type": "Road", "width": int(cell[1:])}
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
            for n, weigth in connected_roads:
                edges[(x,y)].append((n, weigth))
                
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
        
        for node, connections in edges.items():
            for neighbor, weight in connections:
                dot.edge(f"{node[0]},{node[1]}", f"{neighbor[0]},{neighbor[1]}", label=str(weight))
        
        dot.render('road_network', view=True)
    except Exception as e:
        logging.error(str(e))

def main():
    grid=[
        ["B1", "W1", "R2", "R2", "R1"],
        ["R1", "R1", "R2", "R1", "0"],
        ["R1", "R2", "R1", "B2", "R1"],
        ["R2", "W2", "R1", "B2", "B2"],
        ["B3", "B3", "0", "R1", "0"]
    ]
    nodes, edges = identify_IDs(grid)
    if nodes and edges:
        make_graph(nodes, edges)
    else:
        logging.error("Failed to identify nodes or edges.")

if __name__ == "__main__":
    main()