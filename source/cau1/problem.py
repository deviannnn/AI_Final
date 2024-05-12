class Problem:
    def __init__(self, size=8):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'O'

    def __str__(self):
        board_str = "  | "
        board_str += " | ".join(str(i) for i in range(self.size)) + " |\n"
        board_str += "-" * ((self.size * 4) + 3) + "\n"

        for i, row in enumerate(self.board):
            board_str += f"{i} | " + " | ".join(row) + " |\n"
            board_str += "-" * ((self.size * 4) + 3) + "\n"

        return board_str

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
    
    def evaluate(self, board):
        current_player = 'X' if self.player(board) == 'O' else 'O'
        player_score = self.evaluate_player(board, current_player)
        return player_score

    def evaluate_player(self, board, current_player):
        opponent_player = 'O' if current_player == 'X' else 'X'
        score = 0
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == opponent_player and not visited[i][j]:
                    streak_horizontal = self.check_streak(board, i, j, opponent_player, 0, 1, visited)
                    streak_vertical = self.check_streak(board, i, j, opponent_player, 1, 0, visited)
                    streak_diagonal_down_right = self.check_streak(board, i, j, opponent_player, 1, 1, visited)
                    streak_diagonal_up_right = self.check_streak(board, i, j, opponent_player, -1, 1, visited)

                    if streak_horizontal > 0:
                        if 0 <= (j-1) < 8:

                            if board[i][j-1] == current_player:
                                score += 5 * streak_horizontal + self.count_empty_spaces_around(board, i, j-1)

                        if 0 <= (j+streak_horizontal) < 8:

                            if board[i][j+streak_horizontal] == current_player:
                                score += 5 * streak_horizontal + self.count_empty_spaces_around(board, i, j+streak_horizontal)

                    if streak_vertical > 0:
                        if 0 <= (i-1) < 8:

                            if board[i-1][j] == current_player:
                                score += 5 * streak_vertical + self.count_empty_spaces_around(board, i-1, j)

                        if 0 <= (i+streak_vertical) < 8:

                            if board[i+streak_vertical][j] == current_player:
                                score += 5 * streak_vertical + self.count_empty_spaces_around(board, i+streak_vertical, j)

                    if streak_diagonal_down_right > 0:
                        if 0 <= (i-1) < 8 and 0 <= (j-1) < 8:

                            if board[i-1][j-1] == current_player:
                                score += 5 * streak_diagonal_down_right + self.count_empty_spaces_around(board, i-1, j-1)

                        if 0 <= (i+streak_diagonal_down_right) < 8 and 0 <= (j+streak_diagonal_down_right) < 8:

                            if board[i+streak_diagonal_down_right][j+streak_diagonal_down_right] == current_player:
                                score += 5 * streak_diagonal_down_right + self.count_empty_spaces_around(board, i+streak_diagonal_down_right, j+streak_diagonal_down_right)

                    if streak_diagonal_up_right > 0:
                        if 0 <= (i+1) < 8 and 0 <= (j-1) < 8:

                            if board[i+1][j-1] == current_player:
                                score += 5 * streak_diagonal_up_right + self.count_empty_spaces_around(board, i+1, j-1)

                        if 0 <= (i-streak_diagonal_up_right) < 8 and 0 <= (j+streak_diagonal_up_right) < 8:

                            if board[i-streak_diagonal_up_right][j+streak_diagonal_up_right] == current_player:
                                score += 5 * streak_diagonal_up_right + self.count_empty_spaces_around(board, i-streak_diagonal_up_right, j+streak_diagonal_up_right)

        return score

    def count_empty_spaces_around(self, board, x, y):
        empty_spaces_count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Bỏ qua trường hợp x,y chính là ô hiện tại
                new_x, new_y = x + dx, y + dy
                while 0 <= new_x < self.size and 0 <= new_y < self.size and board[new_x][new_y] == ' ':
                    empty_spaces_count += 1
                    new_x += dx
                    new_y += dy
        return empty_spaces_count

        
    def count_consecutive_pieces(self, board, x, y, player, visited):
        score = 0

        # Kiểm tra các chuỗi quân cờ ngang
        streak_horizontal = self.check_streak(board, x, y, player, 0, 1, visited)
        if streak_horizontal >= 2:
            score += streak_horizontal * 10
        
        # Kiểm tra các chuỗi quân cờ dọc
        streak_vertical = self.check_streak(board, x, y, player, 1, 0, visited)
        if streak_vertical >= 2:
            score += streak_vertical * 10
        
        # Kiểm tra các chuỗi quân cờ chéo xuống (phải dưới)
        streak_diagonal_down_right = self.check_streak(board, x, y, player, 1, 1, visited)
        if streak_diagonal_down_right >= 2:
            score += streak_diagonal_down_right * 10

        # Kiểm tra các chuỗi quân cờ chéo lên (phải trên)
        streak_diagonal_up_right = self.check_streak(board, x, y, player, -1, 1, visited)
        if streak_diagonal_up_right >= 2:
            score += streak_diagonal_up_right * 10

        return score

    def check_streak(self, board, x, y, player, dx, dy, visited):
        streak = 1
        visited[x][y] = True  # Đánh dấu ô hiện tại đã được xem xét
        # Kiểm tra các ô tiếp theo trong hướng đã xác định
        for i in range(1, 5):
            new_x = x + i * dx
            new_y = y + i * dy

            # Kiểm tra xem ô mới có nằm trong phạm vi của bàn cờ không
            if 0 <= new_x < 8 and 0 <= new_y < 8:

                # Kiểm tra nếu ô mới chứa quân cờ của player hiện tại
                if board[new_x][new_y] == player:
                    streak += 1
                    visited[new_x][new_y] = True  # Đánh dấu ô mới đã được xem xét
                else:
                    break  # Ngắt nếu không phải quân cờ của player hiện tại
            else:
                break  # Ngắt nếu vượt quá giới hạn của bàn cờ

        return streak



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