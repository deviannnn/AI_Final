from problem import Problem

class AlphaBetaSearch:
    @staticmethod
    def alpha_beta_search(p: Problem):
        actions = p.actions(p.get_board())
        v = float("-inf")
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        for action in actions:
            min_value  = AlphaBetaSearch.min_value(p, p.result(action, p.get_board()), alpha, beta, 1)

            if min_value > v:
                v = min_value
                best_action = action
            alpha = min(alpha, v)

            print("action", action,  "-> min_value", min_value)
        return best_action

    @staticmethod
    def max_value(problem: Problem, board, alpha, beta, depth):
        if problem.terminal(board) or depth == 0:
            # return problem.utility(board)
            return problem.evaluate(board)
        v = float('-inf')
        for action in problem.actions(board):
            v = max(v, AlphaBetaSearch.min_value(problem, problem.result(action, board), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    @staticmethod
    def min_value(problem: Problem, board, alpha, beta, depth):
        if problem.terminal(board) or depth == 0:
            # return problem.utility(board)
            return problem.evaluate(board)
        v = float('inf')
        for action in problem.actions(board):
            v = min(v, AlphaBetaSearch.max_value(problem, problem.result(action, board), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v