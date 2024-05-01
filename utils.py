# function that extracts the txt file data
import networkx as nx
import time

def extract_data(file_number):
    f = open(f'tables/{file_number}.txt', 'r')
    return f.read()

# Function that returns the 1st node that has not been visited yet by BFS algo
# Usefull for the unconnected algo
def unvisited(visited, nodes):


    for i in range(0,len(nodes)):
        if nodes[i] not in visited:
            time.sleep(0.2)
            return nodes[i]


    return ""
