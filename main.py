import menu
import utils
from or_logics import Problem, TransportationProposal


def main() :
    #menu.menu()
    raw_problem_data = utils.extract_data(5)
    pb = Problem(raw_problem_data,5)
    pb.print_transportation_proposals()
    Tp = TransportationProposal(pb)
    Tp.baas_hammer_initialization2()
    Tp.print_transportation_proposal()



#Basically indicates that if the file is runned, it should start the main function.
if __name__ == '__main__' :
    main()