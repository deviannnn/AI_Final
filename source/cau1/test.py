from problem import Problem
from search import AlphaBetaSearch

def main():
    problem = Problem(size = 8)
    while True:
        print(problem)

        if problem.current_player == 'X':
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

        if problem.terminal(problem.board):
            print(problem)
            print("Game over!")
            break

        problem.swap_player()

if __name__ == "__main__":
    main()