

class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42
        self.positions = [5]*7

    # Checks if the winner has been declared already
    def winnerDeclared(self):
        if self.game_result != "":
            return True
        return False

    # Checks if there is a winning move in horizontal direction
    def horizontalWin(self, player):
        for c in range(4):
            for r in range(6):
                if (self.board[r][c] == player and
                   self.board[r][c+1] == player and
                   self.board[r][c+2] == player and
                   self.board[r][c+3] == player):
                    return True
        return False

    # Checks if there is a winning move in vertical direction
    def verticalWin(self, player):
        for c in range(7):
            for r in range(3):
                if (self.board[r][c] == player and
                   self.board[r+1][c] == player and
                   self.board[r+2][c] == player and
                   self.board[r+3][c] == player):
                    return True
        return False

    # Checks if there is a winning move in positive/negative slope diagonal
    def diagonalWin(self, player):
        for c in range(4):
            for r in range(3):
                if (self.board[r][c] == player and
                   self.board[r+1][c+1] == player and
                   self.board[r+2][c+2] == player and
                   self.board[r+3][c+3] == player):
                    return True
        for c in range(4):
            for r in range(3, 6):
                if (self.board[r][c] == player and
                   self.board[r-1][c+1] == player and
                   self.board[r-2][c+2] == player and
                   self.board[r-3][c+3] == player):
                    return True
        return False

    # Checks if the move is a winning move
    def isWinner(self, player_name):
        if player_name == 'p1':
            player = self.player1
        else:
            player = self.player2

        if (self.horizontalWin(player) or self.verticalWin(player) or
           self.diagonalWin(player)):
            self.game_result = player_name
            return True

        return False

    # Checks if the current turn is played by the player who clicked
    def players_turn(self, player_name):
        if self.current_turn != player_name:
            return False
        return True

    # Checks if it is a draw
    def isDraw(self):
        if self.remaining_moves == 0:
            return True
        return False

    # Checks if there is space left in the column clicked
    def isCurrentColumnFilled(self, pos):
        if self.positions[pos] == -1:
            return True
        return False

    # Updates the board and switches the current turn to other player
    def happyMove(self, player_name, pos):
        if player_name == 'p1':
            self.board[self.positions[pos]][pos] = self.player1
        else:
            self.board[self.positions[pos]][pos] = self.player2
        self.positions[pos] = self.positions[pos]-1
        self.remaining_moves = self.remaining_moves-1
        if player_name == 'p1':
            self.current_turn = 'p2'
        else:
            self.current_turn = 'p1'
        return True
