import sys
import utils
from or_logics import Problem, TransportationProposal


#Function that checks the user input for problem selection.
def check_problem_input(user_input,n) :

    try :
        choice_as_number = int(user_input) 
        if not (choice_as_number >=1 and choice_as_number <= n) :
            return False
        return True
    
    except :
        return False

#Menu function
def menu() :
        print("Please chose a problem to solve (from 1 to 12 included).")

        #Stores user input into the problem_choice variable.
        problem_choice = input("> ")
        if not check_problem_input(problem_choice,12) :
            print("\nPlease make sure your input is correct.")
            print()
            menu()

        #Extracts data from txt file and stores it into the variable.
        raw_problem_data = utils.extract_data(problem_choice)
        # Initialize this data as problem.
        pb = Problem(raw_problem_data, problem_choice)
        pb.print_cost_matrix()
        Tp = TransportationProposal(pb)
        print("Please choose between the North-West (1) or the Balas-Hammer (2) Initialization. ")

        # Stores user input into the problem_choice variable.
        problem_choice = input("> ")
        if not check_problem_input(problem_choice,2) :
            print("\nPlease make sure your input is correct.")
            print()
            menu()
        if problem_choice == "1" :
            Tp.northwest_initialize()
        elif problem_choice == "2" :
            Tp.balas_hammer_initialization2()
        Tp.print_transportation_proposal()
        Tp.transportation_cost()
        print("Do you want to optimize this problem (1), go to another problem (2), or quit the program (3)? ")

        problem_choice = input("> ")
        if not check_problem_input(problem_choice, 3):
            print("\nPlease make sure your input is correct.")
            print()
            menu()

        if problem_choice == "1" :
           #Show the associated graph
            Tp.graph.print_graph()


            # Parameter BOOL -> Display (TRUE) or not (FALSE) details in console
            Tp.graph.unconnected(True)

            # Parameter BOOL -> Display (TRUE) or not (FALSE) details in console
            Tp.graph.check_cycle(False)

            if Tp.graph.check_non_degenerate() is False:
                print("\n\n\t/!\ Transport Proposal is degenerated /!\ ")
                print("\tStarting degenerate stepping stone algorithm ...")
                Tp.degenerate_stepping_stone()
            else:
                print("--> NON DEGENERATED TRANSPORT PROPOSAL")

            print(Tp.graph.get_graph())
            Tp.stepping_stone()
            #Show the associated graph
            Tp.graph.print_graph()

        elif problem_choice == "2" :
            menu()

        elif problem_choice == "3" :
            sys.exit(0)

