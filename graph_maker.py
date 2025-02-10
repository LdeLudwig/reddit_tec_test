import graphviz
import logging
from collections import defaultdict

# Initialize logging
logging.basicConfig(filename='./log/graph_maker.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def random_grid_generator(size_x, size_y):
    pass

def identify_IDs(grid):

    nodes = {}
    edges = defaultdict(list) # Using a defaultdict to handle missing keys
    try: 
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                cell = grid[x][y]

                # Check if the cell is a building, storage, or road
                if cell.startswith("B"):
                   nodes[(x,y)] = {"type": "Building", "id": cell}

                elif cell.startswith("S"):
                   nodes[(x,y)] = {"type": "Storage", "id": cell}

                elif cell.startswith("R"):
                   nodes[(x,y)] = {"type": "Road", "weight": cell[1:]}

                else:
                    nodes[(x,y)] = {"type": "Empty"}
        # Identify roads and connect them
        for (x,y), node in nodes.items():
           if node['type'] == 'Road':
                # Check if there are neighboring roads
                neighbors = [(x+dx, y+dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
                # Find roads that are connected to the current road
                connected_road = [n for n in neighbors if n in nodes and nodes[n]['type'] == 'Road']
                for n in connected_road:
                    edges[(x,y)].append((n, nodes[n]['weight']))
        logging.info(f"Nodes: {nodes}, Edges: {edges}")
        return nodes, edges
    except Exception as e:
        logging.error(str(e))
        return None, None


def make_graph(nodes, edges):
    dot = graphviz.Digraph(format='png')

    try:
        for (x,y), node in nodes.items():
            if node['type'] == 'Building':
                label = f"{node['id']}"
                dot.node(f"{x},{y}", label, shape='cicle', style='filled', fillcolor='blue')
            
            elif node['type'] == 'Storage':
                label = f"{node['id']}"
                dot.node(f"{x},{y}", label, shape='box', style='filled', fillcolor='red')
            
            elif node['type'] == 'Road':
                label = f"{node['weight']}"
                dot.node(f"{x},{y}", label, shape='diamond', style='filled', fillcolor='green')

        for (node,connections) in edges.items():
            for (neighbor, weight) in connections:
                dot.edge(f"{neighbor[0]}, {neighbor[1]}", f"{neighbor[0]},{neighbor[1]}", label=str(weight))

        dot.render('road_netword', view=True)
    except Exception as e:
        logging.error(str(e))

def main():
    grid=[
        ["B1", "S1", "R1", "R2", "R1"],
        ["R1", "R1", "R2", "R1", "0"],
        ["R1", "R2", "R1", "B2", "R1"],
        ["R2", "S2", "R1", "B2", "B2"],
        ["B3", "B3", "0", "R1", "0"]
    ]
    nodes, edges = identify_IDs(grid)
    if nodes and edges:
        make_graph(nodes, edges)
    else:
        logging.error("Failed to identify nodes or edges.")

    

if __name__ == "__main__":
    main()