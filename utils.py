# function that extracts the txt file data
def extract_data(file_number):
    f = open(f'tables/{file_number}.txt', 'r')
    return f.read()

# Function that returns the 1st node that has not been visited yet by BFS algo
# Usefull for the unconnected algo
def unvisited(visited, nodes):
    for i in range(0,len(nodes)):
        if nodes[i] not in visited:
            return nodes[i]


    return ""

#Function that returns all customer from a (sub)graph
def find_customer(nodes):
    customer=[]
    for i in range(0, len(nodes)):
        if "C" in nodes[i]:
            customer.append(nodes[i])