import random

class Board:
    def __init__(self, size, state=None):
        self.size = size
        if state:
            self.state = state
        else:
            self.state = [[' ' for _ in range(size)] for _ in range(size)]


    def __str__(self):
        state_str = "  | "
        state_str += " | ".join(str(i) for i in range(self.size)) + " |\n"
        state_str += "-" * ((self.size * 4) + 3) + "\n"
        for i, row in enumerate(self.state):
            state_str += f"{i} | " + " | ".join(row) + " |\n"
            state_str += "-" * ((self.size * 4) + 3) + "\n"
        return state_str
    

    # 4 streak for win
    @staticmethod
    def winner(state):
        size = len(state)
        for i in range(size):
            for j in range(size):
                if state[i][j] != ' ':
                    # Check horizontally
                    if j + 3 < size  and state[i][j] == state[i][j + 1] == state[i][j + 2] == state[i][j + 3]:
                        return state[i][j]
                    # Check vertically
                    if i + 3 < size and state[i][j] == state[i + 1][j] == state[i + 2][j] == state[i + 3][j]:
                        return state[i][j]
                    # Check diagonally (down-right)
                    if i + 3 < size and j + 3 < size and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == state[i + 3][j + 3]:
                        return state[i][j]
                    # Check diagonally (up-right)
                    if i - 3 >= 0 and j + 3 < size and state[i][j] == state[i - 1][j + 1] == state[i - 2][j + 2] == state[i - 3][j + 3]:
                        return state[i][j]
        return ' '
    

class Problem:
    X_SYMBOL = 'X'
    O_SYMBOL = 'O'
    BLANK_SYMBOL = ' '

    
    def __init__(self, size = 8):
        self.size = size
        self.board = Board(size = 8)
        self.current_player = Problem.X_SYMBOL
        self.Human_player = Problem.X_SYMBOL
        self.AI_player = Problem.O_SYMBOL
    

    def actions(self, state: Board):
        possible_actions = []
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == Problem.BLANK_SYMBOL:
                    possible_actions.append((i, j))
        random.shuffle(possible_actions)
        return possible_actions


    def result(self, action, state: Board):
        i, j = action
        if not (0 <= i < self.size and 0 <= j < self.size):
            raise ValueError("Action is out of bounds.")
        if state.state[i][j] != Problem.BLANK_SYMBOL:
            raise ValueError("Cell is already occupied.")

        new_state = [row[:] for row in state.state]
        new_state[i][j] = self.next_player_in_state(state)
        return Board(self.size, new_state)
    

    def next_player_in_state(self, state: Board):
        cnt_X = 0
        cnt_O = 0
        for row in state.state:
            cnt_X += row.count(Problem.X_SYMBOL)
            cnt_O += row.count(Problem.O_SYMBOL)
        
        if cnt_X == cnt_O:
            return Problem.X_SYMBOL
        else:
            return Problem.O_SYMBOL
        

    def terminal(self):
        if Board.winner(self.board.state) != Problem.BLANK_SYMBOL:
            return True
        for row in self.board.state:
            if Problem.BLANK_SYMBOL in row:
                return False
        return True
    

    def utility(self, state: Board):
        winner = Board.winner(state.state)
        if winner == Problem.X_SYMBOL:
            return 1
        elif winner == Problem.O_SYMBOL:
            return -1
        else:
            return 0


    def make_move(self, action):
        if self.is_valid_move(action):
            row, col = action
            self.board.state[row][col] = self.current_player
            self.switch_player()
            return True
        return False
    

    def is_valid_move(self, action):
        row, col = action
        return 0 <= row < self.board.size and 0 <= col < self.board.size and self.board.state[row][col] == Problem.BLANK_SYMBOL


    def switch_player(self):
        if self.current_player == Problem.X_SYMBOL:
            self.current_player = Problem.O_SYMBOL
        else:
            self.current_player = Problem.X_SYMBOL


    def evaluate(self, state: Board, action):
        e_AI = self.evaluate_player(state.state, self.AI_player, action)
        e_Human = self.evaluate_player(state.state, self.Human_player, action)
        
        if (self.Human_player == Problem.X_SYMBOL):
            return e_Human - e_AI
        else:
            return e_AI - e_Human 


    def evaluate_player(self, state, current_player, action):
        opponent_player = Problem.O_SYMBOL if current_player == Problem.X_SYMBOL else Problem.X_SYMBOL
        score = 0
        visited = [[False for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == opponent_player and not visited[i][j]:
                    horizontal, score_of_horizontal = self.evaluate_streak_and_score(state, i, j, opponent_player, 0, 1, visited)
                    vertical, score_of_vertical = self.evaluate_streak_and_score(state, i, j, opponent_player, 1, 0, visited)
                    down_right, score_of_down_right = self.evaluate_streak_and_score(state, i, j, opponent_player, 1, 1, visited)
                    up_right, score_of_up_right = self.evaluate_streak_and_score(state, i, j, opponent_player, -1, 1, visited)

                    if horizontal > 0:
                        if 0 <= (j-1) < 8:
                            if state[i][j-1] == current_player:
                                score += score_of_horizontal + self.rank_of_place(i, j-1) + self.attack(state, i, j-1, current_player)

                        if 0 <= (j+horizontal) < 8:
                            if state[i][j+horizontal] == current_player:
                                score += score_of_horizontal + self.rank_of_place(i, j+horizontal) + self.attack(state, i, j+horizontal, current_player)

                    if vertical > 0:
                        if 0 <= (i-1) < 8:
                            if state[i-1][j] == current_player:
                                score += score_of_vertical + self.rank_of_place(i-1, j) + self.attack(state, i-1, j, current_player)

                        if 0 <= (i+vertical) < 8:
                            if state[i+vertical][j] == current_player:
                                score += score_of_vertical + self.rank_of_place(i+vertical, j) + self.attack(state, i+vertical, j, current_player)

                    if down_right > 0:
                        if 0 <= (i-1) < 8 and 0 <= (j-1) < 8:
                            if state[i-1][j-1] == current_player:
                                score += score_of_down_right + self.rank_of_place(i-1, j-1) + self.attack(state, i-1, j-1, current_player)

                        if 0 <= (i+down_right) < 8 and 0 <= (j+down_right) < 8:
                            if state[i+down_right][j+down_right] == current_player:
                                score += score_of_down_right + self.rank_of_place(i+down_right, j+down_right) + self.attack(state, i+down_right, j+down_right, current_player)

                    if up_right > 0:
                        if 0 <= (i+1) < 8 and 0 <= (j-1) < 8:
                            if state[i+1][j-1] == current_player:
                                score += score_of_up_right + self.rank_of_place(i+1, j-1) + self.attack(state, i+1, j-1, current_player)

                        if 0 <= (i-up_right) < 8 and 0 <= (j+up_right) < 8:
                            if state[i-up_right][j+up_right] == current_player:
                                score += score_of_up_right + self.rank_of_place(i-up_right, j+up_right) + self.attack(state, i-up_right, j+up_right, current_player)
                    
        return score if score != 0 else self.rank_of_place(action[0], action[1])


    def rank_of_place(self, x, y):
        score = 0
        for i in range(self.size):
            if i <= x < self.size - i and i <= y < self.size - i:
                score += 5

        return score


    def evaluate_streak_and_score(self, state, x, y, player, dx, dy, visited):
        streak = 1
        visited[x][y] = True  # Đánh dấu ô hiện tại đã được xem xét
        score = 0
        # Kiểm tra các ô tiếp theo trong hướng đã xác định
        for i in range(1, 5):
            new_x, new_y = x + i * dx, y + i * dy
            # Kiểm tra xem ô mới có nằm trong phạm vi của bàn cờ không
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                # Kiểm tra nếu ô mới chứa quân cờ của player hiện tại
                if state[new_x][new_y] == player:
                    streak += 1
                    visited[new_x][new_y] = True  # Đánh dấu ô mới đã được xem xét
                else:
                    break  # Ngắt nếu không phải quân cờ của player hiện tại
            else:
                break  # Ngắt nếu vượt quá giới hạn của bàn cờ

        # Tính điểm dựa trên streak
        if streak == 1:
            score = 10
        elif streak == 2:
            score = 35
        elif streak == 3:
            score = 500
        else:
            score = 1250

        return streak, score


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