from tabulate import tabulate

#Class that will store a problem's data and related functions.
class Problem():
    def __init__(self, data, pb_n) :
        
        #Stores the problem number (ex 1 for the file 1.txt).
        self.__problem_number = pb_n

        #Will store the raw data from file.
        self.__data = data

        #Stores the prices for moving provision from provider_n to client_n.
        self.__cost_matrix = []

        #Stores the provisions for Pn
        self.__provisions = []

        #Stores the orders for Cn
        self.__orders = []

        #Stores the number of providers.
        self.__provider_n = 0

        #Stores the number of clients.
        self.__client_n = 0

        #Builds the required data.
        self.__build()

    #Function that will execute all the functions required to initialize the problem class.
    def __build(self) :

        #Get each line of raw_data.
        lines = self.__data.split("\n")

        #Orders corresponds to the last line of the raw_data (txt file).
        self.__orders = lines[-1].split(" ")
        
        #The number of clients corresponds to the length of the orders table.
        self.__client_n = len(self.__orders)

        #Iterating through the lines table without the last line (orders).
        for line in lines[:len(lines)-1] :

            #Get each column of the raw (separated by a space in the txt file).
            line_content = line.split(" ")

            #Extract prices (the entire line except the last one).
            prices = line_content[:len(line_content)-1]

            #Extract the provision (last value of the line).
            provision = line_content[-1]

            #Appending extracted data to their respective tables.
            self.__cost_matrix.append(prices)
            self.__provisions.append(provision)

        #The number of providers corresponds to the length of the provisions table.
        self.__provider_n = len(self.__provisions)

        """print("Clients :", self.__client_n)
        print("Providers :", self.__provider_n)
        print("Prices :", self.__cost_matrix)
        print("Provisions :", self.__provisions)
        print("Orders :", self.__orders)"""

    #Prints the cost matrix (prices table).
    def print_cost_matrix(self) :
        print("\nCost matrix :\n")
        #Will store the headers of the cost matrix.
        table_header = []

        #Will store each line of the cost matrix.
        table_content = []

        #Top left corner contains the problem's number.
        table_header.append(self.__problem_number)
        
        #Adding each client to the header.
        for client_n in range(self.__client_n) :
            table_header.append(f"Client {client_n+1}")

        #Adding each provider and their prices to the cost matrix.
        for provider_n in range(self.__provider_n) :
            row = self.__cost_matrix[provider_n].copy()
            row.insert(0, f"Provider {provider_n+1}")
            table_content.append(row)

        #Prints the table in the terminal.
        print(tabulate(table_content, headers=table_header, tablefmt="simple_grid"))

    #Prints the Transportation proposal table
    def print_transportation_proposals(self) :
        print("\Transportation Proposal matrix :\n")
        #Will store the headers of the Transportation Proposal matrix.
        table_header = []

        #Will store each line of the Transportation Proposal matrix.
        table_content = []

        #Top left corner contains the problem's number.
        table_header.append(self.__problem_number)

        #Adding each client to the header.
        for client_n in range(self.__client_n) :
            table_header.append(f"Client {client_n+1}")

        #Top right corners just displays "provisions".
        table_header.append("Provisions")

        #Adding each provider and their prices to the cost matrix.
        for provider_n in range(self.__provider_n) :
            row = []
            row.append(f"Provider {provider_n+1}")

            #Iterating through the cost matrix to fill each row.
            for price in self.__cost_matrix[provider_n] :
                row.append(f"{price}\n____\n0")
            
            #Adding the provision for each provider
            row.append(self.__provisions[provider_n])

            table_content.append(row)

        last_row = []

        #Adding orders to last row.
        last_row = self.__orders.copy()

        #Bottom left corner just displays "Order".
        last_row.insert(0, "Order")

        #Will store the total of orders.
        total_orders = 0

        #computing the total of orders.
        for order in self.__orders :
            total_orders += int(order)

        #Adding the total of orders to the last row.
        last_row.append(total_orders)

        #Adding last row which contains the orders
        table_content.append(last_row)

        #Prints the table in the terminal.
        print(tabulate(table_content, headers=table_header, tablefmt="simple_grid"))
