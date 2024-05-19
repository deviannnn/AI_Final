from problem import Problem
from search import AlphaBetaSearch

def main():
    problem = Problem()

    print("Do you want to choose X or O?\n 1: X\t2: O")
    choose = int(input())

    if choose == 1:
        problem.Human_player = Problem.X_SYMBOL
        problem.AI_player = Problem.O_SYMBOL
    else:
        problem.Human_player = Problem.O_SYMBOL
        problem.AI_player = Problem.X_SYMBOL

    while True:
        print(problem.board)

        if problem.current_player == problem.AI_player:
            action = AlphaBetaSearch.alpha_beta_search(problem)
            problem.make_move(action)
            print(f"Computer places {problem.current_player} at {action}")
        else:
            while True:
                action = tuple(map(int, input("Enter row and column: ").split()))
                if problem.make_move(action) is True:
                    break
                else:
                    print("Invalid move. Please try again!")

        if problem.terminal():
            print(problem.board)
            print("Game over!")
            break

if __name__ == "__main__":
    main()