import networkx as nx
import matplotlib.pyplot as plt
import time
import utils
class Graph():
    def __init__(self, name, provider_nb, client_nb, weight) :

        # graph initialization
        self._graph = nx.Graph()

        # graph's name.
        self._name = name

        # provider number
        self._provider_nb=provider_nb

        # client number
        self._client_nb=client_nb

        # transportation proposal
        self._weight=weight

        # check cycle boolean
        self._cycle = False

    def build_graph(self):

        # Step 1 - Add the nodes to the graph
        # Creating provider nodes
        for i in range(1,self._provider_nb+1):
            node_name = "P" + str(i)
            self._graph.add_node(node_name)

        # Creating Client nodes
        for i in range(1, self._client_nb + 1):
            node_name = "C" + str(i)
            self._graph.add_node(node_name)

        # Step 2 - Connect the nodes between each others & Add weight
        for i in range(self._provider_nb):
            for j in range(self._client_nb):
                if(self._weight[i][j])!=0:
                    node1= "P" + str(i+1)
                    node2= "C" + str(j+1)
                    self._graph.add_edge(node1,node2,weight=self._weight[i][j])


    def print_graph(self):

        # Build the graph
        self.build_graph()

        # Create the plot interface
        fig, ax = plt.subplots(figsize=(10, 7))

        # Position dictionary
        pos = {}

        # Place provider nodes in one row at y = 1
        spacing_x = 1.0 / (self._provider_nb + 1)
        for i in range(1, self._provider_nb + 1):
            pos['P' + str(i)] = (i * spacing_x, 1)  # Adjust y to be 1 for all P nodes

        # Place client nodes in another row at y = 0
        spacing_x = 1.0 / (self._client_nb + 1)
        for i in range(1, self._client_nb + 1):
            pos['C' + str(i)] = (i * spacing_x, 0)  # Adjust y to be 0 for all C nodes

        # Draws the graph on the plot.
        nx.draw(self._graph, pos, ax=ax, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k',
                font_size=16, font_color="black")

        # Indicate to use the weights as edge label.
        edge_labels = nx.get_edge_attributes(self._graph, 'weight')

        # Draws the edges.
        nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=edge_labels)

        # Sets the plot title.
        ax.set_title(self._name + " Visual Representation", fontsize=20, fontweight='bold')

        # Sets the plot windows name.
        plt.get_current_fig_manager().set_window_title('Graph Visualization Window')

        plt.show()

    def breadth_first_algo(self,starting_node):

        print("\n\n\t---- Starting Breadth First Search (BFS) ---\n\n ")
        print("\t** Initial Node: ",starting_node," **")
        queue = []
        visited = []

        # Parent dictionary to store the parent of each node
        # Data Structure : {'P1': [], 'P2': [], 'P3': [], 'C1': [], 'C2': [], 'C3': [], 'C4': []}
        parent = {}

        # Initialization of parent
        for i in range(1, self._provider_nb+1):
            parent["P"+str(i)]=""
        for i in range(1, self._client_nb+1):
            parent["C"+str(i)]=""

        # Initialization of the BFS
        current_node = starting_node
        next_node = ""
        previous_node = starting_node
        queue.append(current_node)
        stop = False
        cpt = 0
        self._cycle = False


        while stop is not True:
            cpt+=1

            # Check cycle
            print("\n\t***** Iteration #",cpt,"*****")
            print("\tCurrent node: ", current_node)
            if current_node in visited and parent[previous_node] != current_node:
                self._cycle = True
                stop = True

            # Step 1 - Store the neighbours in the queue
            neighbors = list(self._graph.neighbors(current_node))

            for i in range (0,len(neighbors)):
                if neighbors[i] not in queue and neighbors[i] not in parent.values():
                    queue.insert(0,neighbors[i])

            print("\tQueue:",queue)

            # Step 2 - Delete current node of the queue (which is the last one)
            print("\tRemoved current node"+current_node)
            queue.pop()
            print("\tQueue updated:",queue)

            # Step 3 -  Next node <=> last element of the queue
            if len(queue) != 0 :
                next_node = queue[-1]
                print("\tNext node:",next_node)

            # Step 4 - Store the current node to the parent
            if next_node != "":
                parent[next_node] = current_node

            visited.append(current_node)
            # Step 5 - Move to the next node
            if next_node == "" :
                stop = True
            else:
                current_node = next_node
                next_node=""
                previous_node = visited[-1]

        return visited, parent

    def unconnected(self):
        print("\n\n\t---- Starting unconnected algorithm ---\n\n ")
        subgraphs = []
        all_visited = []
        starting_node = "P1"

        # Run BFS from the starting node to find the first subgraph
        visited, parent = self.breadth_first_algo(starting_node)
        all_visited.extend(visited)
        subgraphs.append(set(visited))

        # Check for other subgraphs
        connect = all(key in visited for key in parent)
        if not connect:
            #Step 1 - Get the node that is disconnected
            unconnected_node = utils.unvisited(visited, list(parent.keys()))

            while unconnected_node:
                #Step 2 - Rerun the BFS algo
                visited, parent = self.breadth_first_algo(unconnected_node)

                #Step 3 - Add the new visited nodes to the all visited list
                all_visited.extend(visited)

                #Step 4 - Store the subgraph
                subgraphs.append(set(visited))

                #Step 5 - Check if there are other subgraphs
                unconnected_node = utils.unvisited(all_visited, list(parent.keys()))

        if len(subgraphs) > 1:
            print("\n\t/!\ GRAPH UNCONNECTED /!\ ")
            print("\tIDENIFIED",len(subgraphs),"SUBGRAPHS:")
            for i in range(len(subgraphs)):
                print("\t\t* SUBGRAPH #",i+1,": ",subgraphs[i])
            color_map = plt.cm.get_cmap('tab10', len(subgraphs))
            pos = {}
            node_color = {}

            # Position nodes in the same layout as print_graph
            spacing_x = 1.0 / (self._provider_nb + 1)
            for i in range(1, self._provider_nb + 1):
                pos['P' + str(i)] = (i * spacing_x, 1)

            spacing_x = 1.0 / (self._client_nb + 1)
            for i in range(1, self._client_nb + 1):
                pos['C' + str(i)] = (i * spacing_x, 0)

            # Assign a unique color for each node in the subgraph
            for idx, subgraph in enumerate(subgraphs):
                for node in subgraph:
                    node_color[node] = color_map(idx)  # Assign the same color for the entire subgraph

            fig, ax = plt.subplots(figsize=(10, 7))

            # Generate a list of colors for each node based on their color mapping
            color_list = [node_color.get(node, 'gray') for node in self._graph.nodes()]

            nx.draw(self._graph, pos, ax=ax, with_labels=True, node_color=color_list, node_size=2000, edge_color='k',
                    font_size=16, font_color="black")
            edge_labels = nx.get_edge_attributes(self._graph, 'weight')
            nx.draw_networkx_edge_labels(self._graph, pos, edge_labels=edge_labels)
            ax.set_title(f"All Subgraphs Visual Representation", fontsize=20, fontweight='bold')
            plt.get_current_fig_manager().set_window_title('All Subgraphs Visualization')
            plt.show()
        else:
            print("\n\t--> GRAPH CONNECTED")


    # For checking cycle, we assume that the graph is already connected
    def check_cycle(self):
        print("\n\n\t---- Starting cycle algorithm ---\n\n ")
        # Step 1 - Perform BFS
        self.breadth_first_algo("P1")

        # Step 2 - Return Result
        if self._cycle is True:
            print("\n\t/!\ CYCLE DETECTED /!\ ")
            return self._cycle
        else:
            print("\n\t--> NO CYCLE DETECTED")
            return self._cycle
