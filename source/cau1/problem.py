class Problem:
    def __init__(self, size=8):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'

    def print(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * 31)

    def get_board(self):
        return self.board

    def player(self, board):
        X = 'X'
        O = 'O'
        cnt_X = 0
        cnt_o = 0

        for i in range(self.size):
            for j in range(self.size): 
                if board[i][j] == X:
                    cnt_X += 1
                elif board[i][j] == O:
                    cnt_o += 1

        if cnt_X == cnt_o:
            return X
        elif cnt_X > cnt_o:
            return O
        else:
            return X
            
    def actions(self, board):
        possible_actions = []
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == ' ':
                    possible_actions.append((i, j))
        return possible_actions

    def result(self, action, board):
        i, j = action
        new_board = [row[:] for row in board]
        new_board[i][j] = self.player(board)
        return new_board

    '''
    #3x3 winner
    def winner(self, board):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2]:
                if board[i][0] != ' ':
                    return board[i][0]
            
            if board[0][i] == board[1][i] == board[2][i]:
                if board[0][i] != ' ':
                    return board[0][i]

        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] != ' ':
                return board[0][0]
        if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] != ' ':
                return board[0][2]
        
        return ' '
    '''

    #4x4 winner
    def winner(self, board):
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] != ' ':
                    # Check horizontally
                    if j + 3 < self.size and board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3]:
                        return board[i][j]
                    # Check vertically
                    if i + 3 < self.size and board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]:
                        return board[i][j]
                    # Check diagonally (down-right)
                    if i + 3 < self.size and j + 3 < self.size and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                        return board[i][j]
                    # Check diagonally (up-right)
                    if i - 3 >= 0 and j + 3 < self.size and board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3]:
                        return board[i][j]
        return ' '

    def terminal(self, board):
        if self.winner(board) != ' ':
            return True
        else:
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] == ' ':
                        return False
            return True
    
    def utility(self, board):
        if self.winner(board) == 'X':
            return 1
        elif self.winner(board) == 'O':
            return -1
        else:
            return 0

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' '

    def make_move(self, action):
        row, col = action
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            return True
        return False

    # def check_winner(self):
    #     for i in range(8):
    #         for j in range(5):
    #             if (self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] == self.current_player) or \
    #                (self.board[j][i] == self.board[j+1][i] == self.board[j+2][i] == self.board[j+3][i] == self.current_player):
    #                 return True

    #     for i in range(5):
    #         for j in range(5):
    #             if (self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.current_player) or \
    #                (self.board[i][j+3] == self.board[i+1][j+2] == self.board[i+2][j+1] == self.board[i+3][j] == self.current_player):
    #                 return True
    #     return False

    # def play(self):
    #     while True:
    #         self.display_board()
    #         row, col = map(int, input(f"Player {self.current_player}, enter row and column (0-{self.size-1}): ").split())
    #         if self.make_move(row, col):
    #             winner = self.check_winner()
    #             if winner:
    #                 self.display_board()
    #                 print(f"Player {self.current_player} wins!")
    #                 break
    #             self.current_player = 'O' if self.current_player == 'X' else 'X'
    #         else:
    #             print("Invalid move. Try again.")

    # def is_terminal(self, board):
    #     for i in range(3):
    #         if (board[i][0] == board[i][1] == board[i][2] == self.current_player) or \
    #             (board[0][i] == board[1][i] == board[2][i] == self.current_player):
    #             return True

    #     if (board[0][2] == board[1][1] == board[2][0] == self.current_player) or \
    #         (board[0][0] == board[1][1] == board[2][2] == self.current_player):
    #         return True
    #     return False

    # def is_terminal(self, board):
    #     for i in range(8):
    #         for j in range(5):
    #             if (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == self.current_player) or \
    #                (board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] == self.current_player):
    #                 return True

    #     for i in range(5):
    #         for j in range(5):
    #             if (board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == self.current_player) or \
    #                (board[i][j+3] == board[i+1][j+2] == board[i+2][j+1] == board[i+3][j] == self.current_player):
    #                 return True
    #     return False

    # def utility(self, board):
    #     if self.is_terminal(board):
    #         return 10 if self.current_player == 'X' else -10
    #     return 0