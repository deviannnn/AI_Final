from problem import Problem, Board

class AlphaBetaSearch:
    @staticmethod
    def alpha_beta_search(p: Problem):
        actions = p.actions(p.board.state)

        v = float("-inf")
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        for action in actions:
            min_value  = AlphaBetaSearch.min_value(p, p.result(action, p.board), action, alpha, beta, 0)

            if min_value > v:
                v = min_value
                best_action = action
            
            print(action, "->", min_value)

        return best_action

    @staticmethod
    def max_value(problem: Problem, board: Board, action, alpha, beta, depth):
        if problem.terminal() or depth == 0:
            return problem.evaluate(board, action)
        
        v = float('-inf')
        for action in problem.actions(board.state):
            v = max(v, AlphaBetaSearch.min_value(problem, problem.result(action, board), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    @staticmethod
    def min_value(problem: Problem, board: Board, action, alpha, beta, depth):
        if problem.terminal() or depth == 0:
            return problem.evaluate(board, action)
        
        v = float('inf')
        for action in problem.actions(board.state):
            v = min(v, AlphaBetaSearch.max_value(problem, problem.result(action, board), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v