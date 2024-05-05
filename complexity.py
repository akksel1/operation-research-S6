import time
import random

from matplotlib import pyplot as plt


def northwest_initialize(orders,provisions,cost_matrix,n):
    sent_amount = []
    for provider_n in range(n):
        sent_amount.append([])
        for client_n in range(n):
            sent_amount[provider_n].append(0)
    i = -1
    int_provisions = [int(x) for x in provisions]
    int_orders = [int(x) for x in orders]
    orders_copy = orders.copy()
    for constraints in cost_matrix:
        j = 0
        i += 1
        if int_provisions[i] != " ":
            for constraint in constraints:
                if int_provisions[i] > 0 and int_orders[j] > 0:
                    if int_orders[j] - int_provisions[i] > 0:
                        sent_amount[i][j] = int_provisions[i]
                        int_orders[j] = int_orders[j] - int_provisions[i]
                        int_provisions[i] = 0
                    else:
                        sent_amount[i][j] = int_orders[j]
                        int_provisions[i] = int_provisions[i] - int_orders[j]
                        int_orders[j] = 0
                else:
                    sent_amount[i][j] = 0
                j += 1
def penalties_computation(orders,provisions,cost_matrix,sent_amount):
        penalties_order = []
        penalties_provisions = []

        int_orders = [int(x) for x in orders]
        int_provisions = [int(x) for x in provisions]

        # Compute penalties for orders (columns)
        for j in range(0,len(int_orders)):
         if int_orders[j] > 0:
            list_cost = [(i, int(cost_matrix[i][j])) for i in range(len(int_provisions))]
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
                    sent_amount[list_cost[0][0]][j]= int_orders[j]
                    orders[j] = 0
                    int_orders[j] = 0

        # Compute penalties for provisions (rows)
        for j in range(len(int_provisions)):
          if int_provisions[j] > 0:
            list_cost = [(i, int(cost_matrix[j][i])) for i in range(len(int_orders))]
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
                    sent_amount[j][list_cost[0][0]]= int_provisions[j]
                    provisions[j] = 0
                    int_provisions[j] = 0

        return penalties_order, penalties_provisions

def balas_hammer_initialization2(provisions,orders,cost_matrix,n):
        sent_amount = []
        for provider_n in range(n):
            sent_amount.append([])
            for client_n in range(n):
                sent_amount[provider_n].append(0)
        # convert strings to integers for provisions  list and orders list
        int_provisions = [int(x) for x in provisions]
        int_orders = [int(x) for x in orders]

        # while there are still provisions and orders to attribute
        while any(int_provisions) and any(int_orders):
            # computation of the penalties
            col_penalties, row_penalties = penalties_computation(orders,provisions,cost_matrix,sent_amount)


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
                -x[0], cost_matrix[x[1]][x[2]], -min(int_provisions[x[1]], int_orders[x[2]])))
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
                        if cost_matrix[best_row_penalty[1]][best_row_penalty[2]] <= \
                                cost_matrix[best_col_penalty[1]][best_col_penalty[2]]:
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
                sent_amount[i][j] += amount
                int_provisions[i] -= amount
                int_orders[j] -= amount
                # Update the string lists after each transaction
                provisions[i] = str(int_provisions[i])
                orders[j] = str(int_orders[j])
def generate_random_values(n):
    # Generate random orders list
    orders = [random.randint(1, 100) for _ in range(n)]

    # Generate random provisions list
    provisions = [random.randint(1, 100) for _ in range(n)]

    # Generate random 2D cost matrix
    cost_matrix = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    return orders, provisions, cost_matrix

def complexity_northwest_initial(n):
    execution_times = []

    for i in range(100):  # Measure execution time 10 times
        orders, provisions, cost_matrix = generate_random_values(n)
        start_time = time.process_time()
        northwest_initialize(orders,provisions,cost_matrix,n)
        end_time = time.process_time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        print(i)

    return execution_times


def complexity_balas_initial(n):
    execution_times = []

    for i in range(100):  # Measure execution time 10 times
        orders, provisions, cost_matrix = generate_random_values(n)
        start_time = time.process_time()
        balas_hammer_initialization2(orders,provisions,cost_matrix,n)
        end_time = time.process_time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        print(i)

    return execution_times

def plot_complexity(execution_times, execution_times2):

    x_values = range(1, len(execution_times) + 1)

    # Tracer le graphique à dispersion pour la fonction bleue
    plt.scatter(x_values, execution_times, color='blue', label='North-West')

    # Tracer le graphique à dispersion pour la fonction rouge
    plt.scatter(x_values, execution_times2, color='red', label='Balas-Hammer')

    plt.xlabel('Execution Iteration')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Scatter Plot of Execution Times')
    plt.legend()  # Afficher la légende pour les deux fonctions
    plt.show()



def main() :
    plot_complexity(complexity_northwest_initial(400),complexity_balas_initial(400))

if __name__ == '__main__' :
    main()
