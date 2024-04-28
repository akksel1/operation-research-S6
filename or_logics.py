from tabulate import tabulate

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
    def northwest_initialize(self):
        i = 0
        provisions = 0
        initial_cost = [[0 for j in range(len(self.provisions))] for i in range(len(self.orders))]
        orders_copy = self.orders.copy()
        for constraints in self.cost_matrix:
            j = 0
            i += 1
            if self.provisions[i-1] != " ":
                provisions += int(self.provisions[i-1])
                for constraint in constraints:
                    orders = int(orders_copy[j])
                    j +=1
                    if provisions > 0 :
                        if orders - provisions > 0:
                            initial_cost[i-1][j-1] = provisions
                            provisions = 0
                            orders_copy[j-1] = str(int(orders_copy[j-1]) - provisions)
                        else:
                            initial_cost[i-1][j-1] = orders
                            provisions -= orders
                            orders_copy[j-1] = str(int(orders_copy[j-1]) - orders)
                    else:
                        initial_cost[i-1][j-1] = 0
        print(initial_cost)
        return(initial_cost)
        
class TransportationProposal():

    def __init__(self, pb: Problem) :
        
        #Related problem.
        self.__problem = pb

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




