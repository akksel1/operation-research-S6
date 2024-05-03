from tabulate import tabulate
import copy

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
        #Will store the amount of suplly sent each providers to each clients.
        self.__sent_amount = []

        #Function executed to initialize data.
        self.__build()
    
    #Initializing the TransportationProposal data.
    def __build(self):
        #When initialized all sent amounts are 0.
        for provider_n in range(self.__problem.provider_n) :
            self.__sent_amount.append([])
            for client_n in range(self.__problem.client_n) :
                self.__sent_amount[provider_n].append(0)
    
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

    def northwest_initialize(self):
        print(self.__sent_amount)
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

    def baas_hammer_initialization2(self):
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

        return total_cost

    def get_sent_amount(self):
        return self.__sent_amount

