from problem import Problem, Board

class AlphaBetaSearch:
    @staticmethod
    def alpha_beta_search(p: Problem):
        actions = p.actions(p.board.state)

        best_action = None
        alpha = float("-inf")
        beta = float("inf")
        v = float("-inf") if p.AI_player == Problem.X_SYMBOL else float("inf")

        for action in actions:
            if p.AI_player == Problem.X_SYMBOL:
                min_value = AlphaBetaSearch.min_value(p, p.result(action, p.board), action, alpha, beta, 2)
                if min_value > v:
                    v = min_value
                    best_action = action
            else:
                max_value = AlphaBetaSearch.max_value(p, p.result(action, p.board), action, alpha, beta, 2)
                if max_value < v:
                    v = max_value
                    best_action = action

        return best_action

    @staticmethod
    def max_value(problem: Problem, board: Board, _action, alpha, beta, depth):
        if problem.terminal() or depth == 0:
            return problem.evaluate(board, _action)
        
        v = float('-inf')
        for action in problem.actions(board.state):
            v = max(v, AlphaBetaSearch.min_value(problem, problem.result(action, board), action, alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    @staticmethod
    def min_value(problem: Problem, board: Board, _action, alpha, beta, depth):
        if problem.terminal() or depth == 0:
            return problem.evaluate(board, _action)
        
        v = float('inf')
        for action in problem.actions(board.state):
            v = min(v, AlphaBetaSearch.max_value(problem, problem.result(action, board), action, alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v