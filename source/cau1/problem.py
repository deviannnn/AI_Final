class Problem:
    def __init__(self, size=8):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.AI_player = 'X'

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
    
    def swap_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def evaluate(self, board, action):
        return self.evaluate_player(board, self.AI_player, action)


    def evaluate_player(self, board, current_player, action):
        opponent_player = 'O' if current_player == 'X' else 'X'
        score = 0
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == opponent_player and not visited[i][j]:
                    horizontal = self.check_streak(board, i, j, opponent_player, 0, 1, visited)
                    vertical = self.check_streak(board, i, j, opponent_player, 1, 0, visited)
                    down_right = self.check_streak(board, i, j, opponent_player, 1, 1, visited)
                    up_right = self.check_streak(board, i, j, opponent_player, -1, 1, visited)

                    score_of_horizontal = self.score_of_streak(horizontal)
                    score_of_vertical = self.score_of_streak(vertical)
                    score_of_down_right = self.score_of_streak(down_right)
                    score_of_up_right = self.score_of_streak(up_right)

                    
                    if horizontal > 0:
                        if 0 <= (j-1) < 8:
                            if board[i][j-1] == current_player:
                                score += score_of_horizontal + self.rank_of_place(i, j-1) + self.attack(board, i, j - 1, current_player)

                        if 0 <= (j+horizontal) < 8:
                            if board[i][j+horizontal] == current_player:
                                score += score_of_horizontal + self.rank_of_place(i, j+horizontal) + self.attack(board, i, j+horizontal, current_player)

                    if vertical > 0:
                        if 0 <= (i-1) < 8:
                            if board[i-1][j] == current_player:
                                score += score_of_vertical + self.rank_of_place(i-1, j) + self.attack(board, i-1, j, current_player)

                        if 0 <= (i+vertical) < 8:
                            if board[i+vertical][j] == current_player:
                                score += score_of_vertical + self.rank_of_place(i+vertical, j) + self.attack(board, i+vertical, j, current_player)

                    if down_right > 0:
                        if 0 <= (i-1) < 8 and 0 <= (j-1) < 8:
                            if board[i-1][j-1] == current_player:
                                score += score_of_down_right + self.rank_of_place(i-1, j-1) + self.attack(board, i-1, j-1, current_player)

                        if 0 <= (i+down_right) < 8 and 0 <= (j+down_right) < 8:
                            if board[i+down_right][j+down_right] == current_player:
                                score += score_of_down_right + self.rank_of_place(i+down_right, j+down_right) + self.attack(board, i+down_right, j+down_right, current_player)

                    if up_right > 0:
                        if 0 <= (i+1) < 8 and 0 <= (j-1) < 8:
                            if board[i+1][j-1] == current_player:
                                score += score_of_up_right + self.rank_of_place(i+1, j-1) + self.attack(board, i+1, j-1, current_player)

                        if 0 <= (i-up_right) < 8 and 0 <= (j+up_right) < 8:
                            if board[i-up_right][j+up_right] == current_player:
                                score += score_of_up_right + self.rank_of_place(i-up_right, j+up_right) + self.attack(board, i-up_right, j+up_right, current_player)
                    
        return score if score != 0 else self.rank_of_place(action[0], action[1])

    def rank_of_place(self, x, y):
        score = 0
        for i in range(self.size):
            if i <= x < self.size - i and i <= y < self.size - i:
                score += 5

        return score
                
    def check_streak(self, board, x, y, opponent, dx, dy, visited):
        streak = 1
        visited[x][y] = True  # Đánh dấu ô hiện tại đã được xem xét
        # Kiểm tra các ô tiếp theo trong hướng đã xác định
        for i in range(1, 5):
            new_x = x + i * dx
            new_y = y + i * dy

            # Kiểm tra xem ô mới có nằm trong phạm vi của bàn cờ không
            if 0 <= new_x < 8 and 0 <= new_y < 8:

                # Kiểm tra nếu ô mới chứa quân cờ của player hiện tại
                if board[new_x][new_y] == opponent:
                    streak += 1
                    visited[new_x][new_y] = True  # Đánh dấu ô mới đã được xem xét

                else:
                    break # Ngắt nếu không phải quân cờ của player hiện tại
            else:
                break  # Ngắt nếu vượt quá giới hạn của bàn cờ

        return streak
    
    def score_of_streak(self, streak):
        if streak == 1:
            return 10
        elif streak == 2:
            return 35
        elif streak == 3:
            return 250
        else:
            return 1250

    def attack(self, board, x, y, player):
        streak_score_1 = 5
        streak_score_2 = 25
        streak_score_3 = 125
        streak_score_4 = 1250

        score = 0
        if y + 3 < self.size and player == board[x][y + 1] == board[x][y + 2] == board[x][y + 3]:
            score += streak_score_4

        elif y + 2 < self.size and player == board[x][y + 1] == board[x][y + 2]:
            if  0 < y < 7:
                score += streak_score_3

        elif y + 1 < self.size and player == board[x][y + 1]:
            if 0 < y < 7:
                score += streak_score_2

        else:
            score += streak_score_1


        if x + 3 < self.size and player == board[x + 1][y] == board[x + 2][y] == board[x + 3][y]:
            score += streak_score_4

        elif x + 2 < self.size and player == board[x + 1][y] == board[x + 2][y]:
            if 0 < x < 7:
                score += streak_score_3

        elif x + 1 < self.size and player == board[x + 1][y]:
            if 0 < x < 7:
                score += streak_score_2

        else:
            score += streak_score_1


        if x + 3 < self.size and y + 3 < self.size and player == board[x + 1][y + 1] == board[x + 2][y + 2] == board[x + 3][y + 3]:
            score += streak_score_4

        elif x + 2 < self.size and y + 2 < self.size and player == board[x + 1][y + 1] == board[x + 2][y + 2]:
            if 0 < x < 7 and 0 < y < 7:
                score += streak_score_3

        elif x + 1 < self.size and y + 1 < self.size and player == board[x + 1][y + 1]:
            if 0 < x < 7 and 0 < y < 7:
                score += streak_score_2

        else:
            score += streak_score_1


        if x - 3 >= 0 and y + 3 < self.size and player == board[x - 1][y + 1] == board[x - 2][y + 2] == board[x - 3][y + 3]:
            score += streak_score_4

        elif x - 2 >= 0 and y + 2 < self.size and player == board[x - 1][y + 1] == board[x - 2][y + 2]:
            if 0 < x < 7 and 0 < y < 7:
                score += streak_score_3

        elif x - 1 >= 0 and y + 1 < self.size and player == board[x - 1][y + 1]:
            if 0 < x < 7 and 0 < y < 7:
                score += streak_score_2

        else:
            score += streak_score_1


        return score

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

    
    # def count_empty_spaces_around(self, board, x, y):
    #     empty_spaces_count = 0
    #     for dx in [-1, 0, 1]:
    #         for dy in [-1, 0, 1]:
    #             if dx == 0 and dy == 0:
    #                 continue  # Bỏ qua trường hợp x,y chính là ô hiện tại
    #             new_x, new_y = x + dx, y + dy
    #             while 0 <= new_x < self.size and 0 <= new_y < self.size and board[new_x][new_y] == ' ':
    #                 empty_spaces_count += 1
    #                 new_x += dx
    #                 new_y += dy
    #     return empty_spaces_count