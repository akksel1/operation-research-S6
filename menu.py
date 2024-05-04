import utils
from or_logics import Problem, TransportationProposal
import graph as Graph



#Function that checks the user input for problem selection.
def check_problem_input(user_input) :

    try :
        choice_as_number = int(user_input) 
        if not (choice_as_number >=1 and choice_as_number <= 12) :
            return False
        return True
    
    except :
        return False

#Menu function
def menu() :
    print("Please chose a problem to solve (from 1 to 12 included).")
    
    #Stores user input into the problem_choice variable.
    problem_choice = input("> ")
    if not check_problem_input(problem_choice) :
        print("\nPlease make sure your input is correct.")
        print()
        menu()
    
    #Extracts data from txt file and stores it into the variable.
    raw_problem_data = utils.extract_data(problem_choice)

    #Initialize this data as problem.
    pb = Problem(raw_problem_data, problem_choice)
    pb.print_cost_matrix()

    Tp = TransportationProposal(pb)
    #Tp.northwest_initialize()
    Tp.print_transportation_proposal()
    Tp.baas_hammer_initialization2()
    Tp.print_transportation_proposal()
    print(Tp.transportation_cost())



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

