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
def generate_random_values(n):
    # Generate random orders list
    orders = [random.randint(1, 100) for _ in range(n)]

    # Generate random provisions list
    provisions = [random.randint(1, 100) for _ in range(n)]

    # Generate random 2D cost matrix
    cost_matrix = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    return orders, provisions, cost_matrix

def complexity_northwest_initial(n):
    orders,provisions,cost_matrix = generate_random_values(n)
    execution_times = []

    for i in range(100):  # Measure execution time 10 times
        start_time = time.process_time()
        northwest_initialize(orders,provisions,cost_matrix,n)
        end_time = time.process_time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        print(i)

    plot_complexity(n,execution_times)
def plot_complexity(n,execution_times):

    x_values = range(1, len(execution_times) + 1)
    plt.scatter(x_values, execution_times)
    plt.xlabel('Execution Iteration')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Scatter Plot of Northwest Initial')
    plt.ylim(bottom=0)  # Set the lower limit of y-axis to zero
    plt.show()



def main() :
    complexity_northwest_initial(1000)

if __name__ == '__main__' :
    main()
