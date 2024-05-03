import networkx as nx
import matplotlib.pyplot as plt
import utils


class Graph():
    def __init__(self, name, provider_nb, client_nb, weight):

        # graph initialization
        self._graph = nx.Graph()

        # graph's name.
        self._name = name

        # provider number
        self._provider_nb = provider_nb

        # client number
        self._client_nb = client_nb

        # transportation proposal
        self._weight = weight

        # check cycle boolean
        self._cycle = False

        self._cost = []

    def build_graph(self):

        # Step 1 - Add the nodes to the graph
        # Creating provider nodes
        for i in range(1, self._provider_nb + 1):
            node_name = "P" + str(i)
            self._graph.add_node(node_name)

        # Creating Client nodes
        for i in range(1, self._client_nb + 1):
            node_name = "C" + str(i)
            self._graph.add_node(node_name)

        # Step 2 - Connect the nodes between each others & Add weight
        for i in range(self._provider_nb):
            for j in range(self._client_nb):
                if (self._weight[i][j]) != 0:
                    node1 = "P" + str(i + 1)
                    node2 = "C" + str(j + 1)
                    self._graph.add_edge(node1, node2, weight=self._weight[i][j])

    def get_graph(self) :
        edges_with_weights = list(self._graph.edges(data='weight', default=1))
        return edges_with_weights
    
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

    def breadth_first_algo(self, starting_node, display):
        if display:
            print("\n\n\t---- Starting Breadth First Search (BFS) ---\n\n")
            print("\t** Initial Node: ", starting_node, " **")

        # Initialize queue and visited set
        queue = [starting_node]
        visited = set([starting_node])

        # Parent dictionary
        parent = {}
        for i in range(1, self._provider_nb + 1):
            parent["P" + str(i)] = None
        for i in range(1, self._client_nb + 1):
            parent["C" + str(i)] = None

        parent[starting_node] = None
        self._cycle = False
        cpt = 0

        while queue:
            current_node = queue.pop(0)
            cpt += 1

            if display:
                print("\n\t***** Iteration #", cpt, "*****")
                print("\tCurrent node: ", current_node)
                print("\tVisited Nodes:", visited)
                print("\tParent Mapping:", parent)

            # Step 1 - Iterate over neighbors of the current node
            neighbors = list(self._graph.neighbors(current_node))
            for neighbor in neighbors:
                # If neighbor is not visited, add to queue and set parent
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = current_node
                # If the neighbor is visited and is not the parent of the current node
                elif parent[current_node] != neighbor:
                    self._cycle = True
                    if display:
                        print("\n\t***** CYCLE DETECTED *****")
                        print("\tCycle Involves:", current_node, neighbor)
                    return visited, parent

            if display:
                print("\tQueue:", queue)

        return visited, parent

    #Function that returns TRUE if a graph is unconnected, FALSE if connected
    def unconnected(self,display):
        print("\n\n\t---- Starting unconnected algorithm ---\n\n ")
        subgraphs = []
        all_visited = []
        starting_node = "P1"

        # Run BFS from the starting node to find the first subgraph
        visited, parent = self.breadth_first_algo(starting_node, display)
        all_visited.extend(visited)
        subgraphs.append(set(visited))

        # Check for other subgraphs
        connect = all(key in visited for key in parent)
        if not connect:
            # Step 1 - Get the node that is disconnected
            unconnected_node = utils.unvisited(visited, list(parent.keys()))

            while unconnected_node:
                # Step 2 - Rerun the BFS algo
                visited, parent = self.breadth_first_algo(unconnected_node, display)

                # Step 3 - Add the new visited nodes to the all visited list
                all_visited.extend(visited)

                # Step 4 - Store the subgraph
                subgraphs.append(set(visited))

                # Step 5 - Check if there are other subgraphs
                unconnected_node = utils.unvisited(all_visited, list(parent.keys()))

        if len(subgraphs) > 1:
            print("\n\t/!\ GRAPH UNCONNECTED /!\ ")
            print("\tIDENIFIED", len(subgraphs), "SUBGRAPHS:")
            for i in range(len(subgraphs)):
                print("\t\t* SUBGRAPH #", i + 1, ": ", subgraphs[i])
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
            return True
        else:
            print("\n\t--> GRAPH CONNECTED")
            return False

    #Function that extracts all subgraphs from an unconnected graph
    def get_subgraphs(self):
        all_visited = []
        starting_node = "P1"
        subgraphs = []

        # Run BFS from the starting node to find the first subgraph
        visited, parent = self.breadth_first_algo(starting_node, False)
        all_visited.extend(visited)
        subgraphs.append(set(visited))

        # Check for other subgraphs
        connect = all(key in visited for key in parent)
        if not connect:
            # Step 1 - Get the node that is disconnected
            unconnected_node = utils.unvisited(visited, list(parent.keys()))

            while unconnected_node:
                # Step 2 - Rerun the BFS algo
                visited, parent = self.breadth_first_algo(unconnected_node, False)

                # Step 3 - Add the new visited nodes to the all visited list
                all_visited.extend(visited)

                # Step 4 - Store the subgraph
                subgraphs.append(set(visited))

                # Step 5 - Check if there are other subgraphs
                unconnected_node = utils.unvisited(all_visited, list(parent.keys()))
        return subgraphs

    #Function that returns TRUE if a graph contains cycle, FALSE if not. Notice that this info is stored inside the object self._cycle
    def check_cycle(self,display):
        print("\n\n\t---- Starting cycle algorithm ---")

        subgraphs = list(self.get_subgraphs())

        for i in range(0, len(subgraphs)):
            initial_node = list(subgraphs[i])[0]

            # Step 1 - Perform BFS
            print("\tPerforming BFS to detect any potential cycle...")
            self.breadth_first_algo(initial_node, display)

            # Step 2 - Return Result
            if self._cycle is True:
                print("\t/!\ CYCLE DETECTED /!\ ")
                return self._cycle

        print("\t--> NO CYCLE DETECTED")
        return self._cycle

    # Function that allows stepping stone on a degenerated graph by adding the right edge (min cost)
    def degenerate_stepping_stone(self, cost_matrix, sent_amount):
        if (self._cycle is True):
            print("Cannot proceed degenerate stepping stone method when a cycle appears")
            return

        # Compute the # of edge that needs to be added
        nb_edge = self._graph.number_of_edges()
        nb_node = self._graph.number_of_nodes()

        nb_edge_need = nb_node - nb_edge - 1

        if (nb_edge_need == 0):
            print("\nThe graph is already connected")
            return

        added_edge_cpt = 0

        # Converting cost matrix in int
        for i in range(self._provider_nb):
            for j in range(self._client_nb):
                cost_matrix[i][j] = int(cost_matrix[i][j])

        # Initialize create_cycle matrix
        # -> if 0 : the connection does not  create a cycle
        # -> if 1 : the connection creates a cycle
        create_cycle = []
        for i in range(self._provider_nb):
            a = []
            for j in range(self._client_nb):
                a.append(0)
            create_cycle.append(a)


        # While we have not added all the edges needed, we continue to search for minimum and new connections
        while added_edge_cpt < nb_edge_need:

            #Put '-1' in cost matrix when the connection already exists
            for i in range(self._provider_nb):
                for j in range(self._client_nb):
                    if sent_amount[i][j] !=0 and sent_amount[i][j] > 0 :
                        cost_matrix[i][j] = -1

            # Find the minimum among all others client & positive ! (if -1 it would meant that the edge is existing
            # or it creates a cycle when added)

            # Step 1 - Find the first postive value in matrix (to not take an aritrary value to find min)
            found = False
            # Coordinates of the minimum
            coordinates = []
            while(found is False):
                i=0
                while i < self._provider_nb and found is False:
                    j=0
                    while j < self._client_nb and found is False:
                        if sent_amount[i][j] == 0 and cost_matrix[i][j]>0:
                            found = True
                            minimum = cost_matrix[i][j]
                            coordinates.append(i)
                            coordinates.append(j)
                        j+=1
                    i+=1

            # Step 2 - minimum positive algo
            for i in range(self._provider_nb):
                for j in range(self._client_nb):
                    if minimum > cost_matrix[i][j] and cost_matrix[i][j] > 0:
                        minimum = cost_matrix[i][j]
                        coordinates.append(i)
                        coordinates.append(j)


            # Step 3 - try to connect
            node_provider = "P"+str(coordinates[0]+1)
            node_customer = "C"+str(coordinates[1]+1)
            self._graph.add_edge(node_provider,node_customer,weight=sent_amount[coordinates[0]][coordinates[1]])


            # Step 4 - check cycle
            self.check_cycle(False)

            # If a cycle has been detected -> Del the new edge and put -1 in cost matrix
            if self._cycle is True :
                cost_matrix[coordinates[0]][coordinates[1]] = -1
                coordinates=[]
                self._graph.remove_edge(node_provider,node_customer)
            else:
                #We add the edge !
                cost_matrix[coordinates[0]][coordinates[1]] = -1
                added_edge_cpt +=1


            self.print_graph()

    #Function that returns True if a TP is non-degenerate
    def check_non_degenerate(self):

        #Check cycle
        self.check_cycle(False)

        # Compute the # of edge that needs to be added
        nb_edge = self._graph.number_of_edges()
        nb_node = self._graph.number_of_nodes()

        nb_edge_need = nb_node - nb_edge - 1

        if(nb_edge_need == 0 and self._cycle is False):
            return True
        return False



