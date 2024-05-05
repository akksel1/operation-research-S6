from tabulate import tabulate
import copy
import graph

#Class that will store a problem's data and related functions.
class Problem():
    def __init__(self, data, pb_n) :
        
        #Stores the problem number (ex 1 for the file 1.txt).
        self.problem_number = pb_n

        #Will store the raw data from file.
        self.__data = data

        #Stores the prices for moving provision from provider_n to client_n.
        self.cost_matrix = []

        #Stores the provisions for Pn
        self.provisions = []

        #Stores the orders for Cn
        self.orders = []

        #Stores the number of providers.
        self.provider_n = 0

        #Stores the number of clients.
        self.client_n = 0

        #Builds the required data.
        self.__build()

        self.__transpo = TransportationProposal(self)

    #Function that will execute all the functions required to initialize the problem class.
    def __build(self) :

        #Get each line of raw_data.
        lines = self.__data.split("\n")

        #Orders corresponds to the last line of the raw_data (txt file).
        self.orders = lines[-1].split(" ")
        
        #The number of clients corresponds to the length of the orders table.
        self.client_n = len(self.orders)

        #Iterating through the lines table without the last line (orders).
        for line in lines[:len(lines)-1] :

            #Get each column of the raw (separated by a space in the txt file).
            line_content = line.split(" ")

            #Extract prices (the entire line except the last one).
            prices = line_content[:len(line_content)-1]

            #Extract the provision (last value of the line).
            provision = line_content[-1]

            #Appending extracted data to their respective tables.
            self.cost_matrix.append(prices)
            self.provisions.append(provision)

        #The number of providers corresponds to the length of the provisions table.
        self.provider_n = len(self.provisions)

        """print("Clients :", self.client_n)
        print("Providers :", self.provider_n)
        print("Prices :", self.cost_matrix)
        print("Provisions :", self.provisions)
        print("Orders :", self.orders)"""

    #Prints the cost matrix (prices table).
    def print_cost_matrix(self) :
        print("\nCost matrix :\n")
        #Will store the headers of the cost matrix.
        table_header = []

        #Will store each line of the cost matrix.
        table_content = []

        #Top left corner contains the problem's number.
        table_header.append(self.problem_number)
        
        #Adding each client to the header.
        for client_n in range(self.client_n) :
            table_header.append(f"Client {client_n+1}")

        #Adding each provider and their prices to the cost matrix.
        for provider_n in range(self.provider_n) :
            row = self.cost_matrix[provider_n].copy()
            row.insert(0, f"Provider {provider_n+1}")
            table_content.append(row)

        #Prints the table in the terminal.
        print(tabulate(table_content, headers=table_header, tablefmt="simple_grid"))

    #Prints the Transportation proposal table
    def print_transportation_proposals(self) :
        
        self.__transpo.print_transportation_proposal()

    def get_cost_matrix(self):
        return self.cost_matrix


class TransportationProposal():

    def __init__(self, pb: Problem) :
        
        #Related problem.
        self.__problem = pb

        self.__provisions = copy.deepcopy(pb.provisions)
        self.__orders = copy.deepcopy(pb.orders)

        #Will store the amount of suply sent each providers to each clients.
        self.__sent_amount = []

        self.graph = None

        self.potential_cost_matrix = []

        self.marginal_costs_matrix  = []


        #Function executed to initialize data.
        self.__build()
    
    #Initializing the TransportationProposal data.
    def __build(self):
        #When initialized all sent amounts are 0.
        for provider_n in range(self.__problem.provider_n) :
            self.__sent_amount.append([])
            self.potential_cost_matrix.append([])
            self.marginal_costs_matrix.append([])
            for client_n in range(self.__problem.client_n) :
                self.__sent_amount[provider_n].append(0)
                self.potential_cost_matrix[provider_n].append(0)
                self.marginal_costs_matrix[provider_n].append(0)
        self.__update_graph()

    def __update_graph(self):
        name = "Graph " + self.__problem.problem_number
        self.graph = graph.Graph(name, self.__problem.provider_n, self.__problem.client_n, self.__sent_amount)

    def __print_matrix(self, matrix, display_name) :
        print(display_name)
        table_header = []
        table_content = []

        #Top left corner contains the problem's number.
        table_header.append(self.__problem.problem_number)

        #Adding each client to the header.
        for client_n in range(self.__problem.client_n) :
            table_header.append(f"Client {client_n+1}")

        for provider_n in range(len(matrix)) :
            row = matrix[provider_n].copy()
            row.insert(0, f"Provider {provider_n+1}")
            table_content.append(row)

        print(tabulate(table_content, headers=table_header, tablefmt="simple_grid"))

    def print_potential_costs_matrix(self):
        self.__print_matrix(self.potential_cost_matrix, "\nPotential Costs matrix :\n")

    def print_marginal_costs_matrix(self):
        self.__print_matrix(self.marginal_costs_matrix, "\nMarginal Costs matrix :\n")
        
    
    def degenerate_stepping_stone(self):
        self.graph.degenerate_stepping_stone(copy.deepcopy(self.__problem.cost_matrix), self.__sent_amount)

    def stepping_stone(self, iteration=1) :
        print("\n\nStepping Stone iteration", iteration)
        transportation_graph = self.graph.get_graph()
        #print(transportation_graph)
        client_value = {}
        provider_value = {}
        for edge in transportation_graph :
            provider = edge[0]
            client = edge[1]
            if not provider in provider_value :
                provider_value.update({provider:None})
            if not client in client_value :
                client_value.update({client:None})

        def compute_equations():
            #initialize E(p1)=0
            repass = False
            initial_edge = transportation_graph[0]
            initial_provider = initial_edge[0]
            for edge in transportation_graph :
                provider_value[initial_provider] = 0
                provider = edge[0]
                client = edge[1]
                client_index = int(client[1:len(client)])-1
                provider_index = int(provider[1:len(provider)])-1
                cost = int(self.__problem.cost_matrix[provider_index][client_index])
                
                if client_value[client] == None and provider_value[provider] == None : 
                    repass = True
                else :
                    if client_value[client] == None :
                        client_value[client] = -cost+provider_value[provider]
                    
                    else :
                        provider_value[provider] = cost+client_value[client]
            if repass :
                compute_equations()

        def compute_potential_costs() :
            provider_index = 0
            for provider in provider_value :
                client_index = 0
                for client in client_value :
                    cost = provider_value[provider]-client_value[client]
                    self.potential_cost_matrix[provider_index][client_index] = cost
                    client_index += 1
                provider_index += 1

        def compute_marginal_costs():
            for provider_index in range(len(self.potential_cost_matrix)) :
                for client_index in range(len(self.potential_cost_matrix[provider_index])) :
                    cost = int(self.__problem.cost_matrix[provider_index][client_index]) - self.potential_cost_matrix[provider_index][client_index]
                    self.marginal_costs_matrix[provider_index][client_index] = cost

        def max_transportation(coordinates, cycle) :
            def get_couples() :
                cycle.pop(-1)
                
                couples = []
                for i in range(len(cycle)) :
                    if cycle[i][0] == "C" and i == 0 and cycle[-1][0] == "P" :
                        couples.append([cycle[-1], cycle[i]])
                    if cycle[i][0] == "P" :
                        couples.append([cycle[i], cycle[i-1]])
                        if i < len(cycle)-1 :
                            couples.append([cycle[i], cycle[i+1]])
                return couples
            


            self.graph.print_graph()
            cycle_couples = get_couples()

            print("Cycle Couples", cycle_couples)

            provider_to_max, client_to_max = coordinates
            provider_tag = f"P{provider_to_max+1}"
            client_tag = f"C{client_to_max+1}"

            max_row_values = 0
            max_col_values = 0

            target_tag = [f"P{provider_to_max+1}",f"C{client_to_max+1}"]

            for cli_idx in range(len(self.__sent_amount[provider_to_max])) :
                cli_tag = f"C{cli_idx+1}"
                pro_tag = f"P{provider_to_max+1}"
                if [pro_tag, cli_tag] in cycle_couples  and [pro_tag, cli_tag] != target_tag :
                    print(pro_tag, cli_tag, "in cycle, updating max_row_val.")
                    max_row_values += self.__sent_amount[provider_to_max][cli_idx]

            for pro_idx in range(len(self.__sent_amount)):
                cli_tag = f"C{client_to_max+1}"
                pro_tag = f"P{pro_idx+1}"
                if [pro_tag, cli_tag] in cycle_couples and [pro_tag, cli_tag] != target_tag :
                    print(pro_tag, cli_tag, "in cycle, updating max_col_val.")
                    max_col_values += self.__sent_amount[pro_idx][client_to_max]


            print("Max col val", max_col_values)
            print("Max row val", max_row_values)
            
            max_supply = int(self.__problem.provisions[provider_to_max])
            max_order = int(self.__problem.orders[client_to_max])
            amount_to_add = min(max_supply, max_order, max_row_values, max_col_values)
            if amount_to_add == 0 :
                print("\nCannot maximize", target_tag, " transportation proposal already optimal.")
                return False
            print(f"Maxing {target_tag} with {amount_to_add}")
            self.__sent_amount[provider_to_max][client_to_max] += amount_to_add

            


           
            for index, couple in enumerate(cycle_couples):
                if couple == [provider_tag, client_tag]:
                    max_index = index
                    break
            else:
                raise ValueError("Specified relation is not in the cycle couples.")

           
            before_couple = cycle_couples[max_index - 1] if max_index > 0 else cycle_couples[-1]
            forward_couple = cycle_couples[(max_index + 1) % len(cycle_couples)]

           
            before_prov_idx = int(before_couple[0][1:]) - 1
            before_cli_idx = int(before_couple[1][1:]) - 1
            forward_prov_idx = int(forward_couple[0][1:]) - 1
            forward_cli_idx = int(forward_couple[1][1:]) - 1

            delta = min(
                self.__sent_amount[before_prov_idx][before_cli_idx],
                self.__sent_amount[forward_prov_idx][forward_cli_idx]
            )

            
            coefficient = -1
            for i in range(1, len(cycle_couples)):
                idx = (max_index + i) % len(cycle_couples)
                prov_idx = int(cycle_couples[idx][0][1:]) - 1
                cli_idx = int(cycle_couples[idx][1][1:]) - 1
                self.__sent_amount[prov_idx][cli_idx] += coefficient * delta
                coefficient *= -1  # Alterner le coefficient
                        
                       
            print("Adjusted transportation proposal matrix :")
            self.print_transportation_proposal()

            return True



        def check_negative_mc() :
            
            max_neg = -1
            coordinates = []

            for provider_index in range(len(self.marginal_costs_matrix)) :
                for client_index in range(len(self.marginal_costs_matrix[provider_index])):
                    if self.marginal_costs_matrix[provider_index][client_index] <= max_neg :
                        max_neg = self.marginal_costs_matrix[provider_index][client_index] 
                        coordinates = [provider_index, client_index]
            
            if len(coordinates) > 0 :
                print(f"Negative value ({max_neg}) found at P{coordinates[0]+1}, C{coordinates[1]+1}")
                print("Adding it to the graph.")
                self.graph.add_edge(f"P{coordinates[0]+1}", f"C{coordinates[1]+1}")
                try :
                    cycle = self.graph.get_cycle()[0]
                    cycle.append(cycle[0])
                except :
                    print("\nAdded edge does not create a cycle. Transportation porposal cannot be improved by stepping stone.")
                    return
                
                else :
                    print("Resultant cycle :", cycle)
                    if not max_transportation(coordinates, cycle) :
                        return

                    
                    name = "Graph " + self.__problem.problem_number
                    self.graph = graph.Graph(name, self.__problem.provider_n, self.__problem.client_n, self.__sent_amount)
                    self.graph.print_graph()
                    self.graph.unconnected(False)
                    self.graph.check_cycle(False)

                if self.graph.check_non_degenerate() is False:
                    self.degenerate_stepping_stone()
                
                self.graph.print_graph()
                
                self.stepping_stone(iteration+1)
        
            else :
                print("No negative value in marginal cost table, transportation proposal is optimal.")
                self.print_transportation_proposal()
                
            

        compute_equations()
        #Sorting the dicts.
        client_value = dict(sorted(client_value.items()))
        provider_value = dict(sorted(provider_value.items()))
        #print("\nClient values :",client_value, "\nProvider values :",provider_value)
        compute_potential_costs()
       
        self.print_potential_costs_matrix()

        compute_marginal_costs()
        self.print_marginal_costs_matrix()
        
        print("Checking negative values in Marginal cost matrix")
        check_negative_mc()








    #Prints the Transportation proposal table
    def print_transportation_proposal(self) :

        print("\nTransportation Proposal matrix :\n")
        #Will store the headers of the Transportation Proposal matrix.
        table_header = []

        #Will store each line of the Transportation Proposal matrix.
        table_content = []

        #Top left corner contains the problem's number.
        table_header.append(self.__problem.problem_number)

        #Adding each client to the header.
        for client_n in range(self.__problem.client_n) :
            table_header.append(f"Client {client_n+1}")

        #Top right corners just displays "provisions".
        table_header.append("Provisions")

        #Adding each provider and their prices to the cost matrix.
        for provider_n in range(self.__problem.provider_n) :
            row = []
            row.append(f"Provider {provider_n+1}")

            #Iterating through the cost matrix to fill each row.
            for client_n in range(len(self.__problem.cost_matrix[provider_n])) :
                
                #Getting the price from the cost matrix.
                price = self.__problem.cost_matrix[provider_n][client_n]

                #Getting the sent amount of supply from the sent_amount table.
                associated_supply = self.__sent_amount[provider_n][client_n]

                row.append(f"{price}\n____\n{associated_supply}")
            
            #Adding the provision for each provider
            row.append(self.__problem.provisions[provider_n])

            table_content.append(row)

        #Adding orders to last row.
        last_row = self.__problem.orders.copy()

        #Bottom left corner just displays "Order".
        last_row.insert(0, "Order")

        #Will store the total of orders.
        total_orders = 0

        #computing the total of orders.
        for order in self.__problem.orders :
            total_orders += int(order)

        #Adding the total of orders to the last row.
        last_row.append(total_orders)

        #Adding last row which contains the orders
        table_content.append(last_row)

        #Prints the table in the terminal.
        print(tabulate(table_content, headers=table_header, tablefmt="simple_grid"))
        print("\n")
        self.transportation_cost()


    def northwest_initialize(self):
        i = -1
        int_provisions = [int(x) for x in self.__provisions]
        int_orders = [int(x) for x in self.__orders]
        orders_copy = self.__problem.orders.copy()
        for constraints in self.__problem.cost_matrix:
            j = 0
            i += 1
            if int_provisions[i] != " ":
                for constraint in constraints:
                    if int_provisions[i] > 0 and int_orders[j] > 0:
                        if int_orders[j] - int_provisions[i] > 0:
                            self.__sent_amount[i][j] = int_provisions[i]
                            int_orders[j] = int_orders[j] - int_provisions[i]
                            int_provisions[i] = 0
                        else:
                            self.__sent_amount[i][j] = int_orders[j]
                            int_provisions[i] = int_provisions[i] - int_orders[j]
                            int_orders[j] = 0
                    else:
                        self.__sent_amount[i][j] = 0
                    j += 1

    def penalties_computation(self):
        penalties_order = []
        penalties_provisions = []

        int_orders = [int(x) for x in self.__orders]
        int_provisions = [int(x) for x in self.__provisions]

        # Compute penalties for orders (columns)
        for j in range(0,len(int_orders)):
         if int_orders[j] > 0:
            list_cost = [(i, int(self.__problem.cost_matrix[i][j])) for i in range(len(int_provisions))]
            if len(list_cost) > 1:
                list_cost_copy= list_cost.copy()
                for i in range(0,len(list_cost)):
                    if(int_provisions[i] ==0):
                        list_cost.remove(list_cost_copy[i])
                list_cost.sort(key=lambda x: x[1])
                if(len(list_cost) > 1):
                    penalty = list_cost[1][1] - list_cost[0][1]
                    penalties_order.append((penalty,list_cost[0][0],j))
                elif(len(list_cost) == 1):
                    self.__sent_amount[list_cost[0][0]][j]= int_orders[j]
                    self.__orders[j] = 0
                    int_orders[j] = 0

        # Compute penalties for provisions (rows)
        for j in range(len(int_provisions)):
          if int_provisions[j] > 0:
            list_cost = [(i, int(self.__problem.cost_matrix[j][i])) for i in range(len(int_orders))]
            if len(list_cost) > 1:
                list_cost_copy = list_cost.copy()
                for i in range(0, len(list_cost)):
                    if(int_orders[i] == 0):
                        list_cost.remove(list_cost_copy[i])
                list_cost.sort(key=lambda x: x[1])
                if(len(list_cost) > 1):
                    penalty = list_cost[1][1] - list_cost[0][1]
                    penalties_provisions.append((penalty, j,list_cost[0][0]))
                elif(len(list_cost) == 1):
                    self.__sent_amount[j][list_cost[0][0]]= int_provisions[j]
                    self.__provisions[j] = 0
                    int_provisions[j] = 0

        return penalties_order, penalties_provisions

    def balas_hammer_initialization2(self):
        # convert strings to integers for provisions  list and orders list
        int_provisions = [int(x) for x in self.__provisions]
        int_orders = [int(x) for x in self.__orders]

        # while there are still provisions and orders to attribute
        while any(int_provisions) and any(int_orders):
            # computation of the penalties
            col_penalties, row_penalties = self.penalties_computation()


            # No more valid moves left
            if not row_penalties and not col_penalties:
                break

            # choose the best move when penalties are equal or choose the highest penalty
            def select_best_move(penalties):
                # filter the penalties where order or provisions are 0
                valid_penalties = [penalty for penalty in penalties if
                                   int_provisions[penalty[1]] > 0 and int_orders[penalty[2]] > 0]
                # Sort penalties by highest penalty, lowest cost, and maximum possible fill amount
                valid_penalties.sort(key=lambda x: (
                -x[0], self.__problem.cost_matrix[x[1]][x[2]], -min(int_provisions[x[1]], int_orders[x[2]])))
                return valid_penalties[0] if valid_penalties else None

            # Select the best move based on the sorted penalties
            if row_penalties and col_penalties:
                best_row_penalty = select_best_move(row_penalties)
                best_col_penalty = select_best_move(col_penalties)

                # If no possible move
                if not best_row_penalty and not best_col_penalty:
                    break

                # Choose the best move between the row and the col
                if best_row_penalty and best_col_penalty:
                    if best_row_penalty[0] > best_col_penalty[0]:
                        best_penalty = best_row_penalty
                    elif best_row_penalty[0] < best_col_penalty[0]:
                        best_penalty = best_col_penalty
                    else:
                        # If penalties are equal, compare based on their capacity
                        if self.__problem.cost_matrix[best_row_penalty[1]][best_row_penalty[2]] <= \
                                self.__problem.cost_matrix[best_col_penalty[1]][best_col_penalty[2]]:
                            best_penalty = best_row_penalty
                        else:
                            best_penalty = best_col_penalty
                else:
                    best_penalty = best_row_penalty or best_col_penalty
            elif not col_penalties and len(row_penalties) !=1:
                best_penalty = select_best_move(row_penalties)
            elif not row_penalties and len(col_penalties) != 1:
                best_penalty = select_best_move(col_penalties)
            else:
                break
            # Make the assignment based on the best penalty
            if best_penalty:
                _, i, j = best_penalty
                amount = min(int_provisions[i], int_orders[j])
                self.__sent_amount[i][j] += amount
                int_provisions[i] -= amount
                int_orders[j] -= amount
                # Update the string lists after each transaction
                self.__provisions[i] = str(int_provisions[i])
                self.__orders[j] = str(int_orders[j])


    def transportation_cost(self):
        total_cost =0
        for i in range(0,len(self.__sent_amount)):
            for j in range(0,len(self.__sent_amount[i])):
                total_cost += int(self.__sent_amount[i][j]) * int(self.__problem.cost_matrix[i][j])

        print("Transportation Cost = ", total_cost)

    def get_sent_amount(self):
        return self.__sent_amount

