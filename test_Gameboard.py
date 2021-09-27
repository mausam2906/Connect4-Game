import unittest
from Gameboard import Gameboard

game = Gameboard()


class Test_TestGameboard(unittest.TestCase):

    # Checks if the winner has been declared already
    def test_winnerDeclared(self):
        game = Gameboard()
        game.game_result = ""
        self.assertEqual(game.winnerDeclared(), False)
        game.game_result = "p1"
        self.assertEqual(game.winnerDeclared(), True)

    # Checks if there is a winning move in horizontal direction
    def test_horizontalWin(self):
        game = Gameboard()
        game.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      ["yellow", "yellow", "yellow", 0, 0, 0, 0],
                      ["red", "red", "red", "red", 0, 0, 0]]
        self.assertEqual(game.horizontalWin("red"), True)
        self.assertEqual(game.horizontalWin("yellow"), False)

    # Checks if there is a winning move in vertical direction
    def test_verticalWin(self):
        game = Gameboard()
        game.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      ["red", 0, 0, 0, 0, 0, 0],
                      ["red", "yellow", 0, 0, 0, 0, 0],
                      ["red", "yellow", 0, 0, 0, 0, 0],
                      ["red", "yellow", 0, 0, 0, 0, 0]]
        self.assertEqual(game.verticalWin("red"), True)
        self.assertEqual(game.verticalWin("yellow"), False)

    # Checks if there is a winning move in positive/negative slope diagonal
    def test_diagonalWin(self):
        game = Gameboard()
        game.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, "red", 0, 0, 0],
                      [0, 0, "red", "yellow", 0, 0, 0],
                      [0, "red", "yellow", "yellow", 0, 0, 0],
                      ["red", "yellow", "yellow", "red", "red", 0, 0]]
        self.assertEqual(game.diagonalWin("red"), True)
        self.assertEqual(game.diagonalWin("yellow"), False)
        game.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      ["red", 0, 0, 0, 0, 0, 0],
                      ["yellow", "red", 0, 0, 0, 0, 0],
                      ["yellow", "yellow", "red", 0, 0, 0, 0],
                      ["red", "yellow", "yellow", "red", "red", 0, 0]]
        self.assertEqual(game.diagonalWin("red"), True)
        self.assertEqual(game.diagonalWin("yellow"), False)

    # Checks if the move is a winning move
    def test_isWinner(self):
        game = Gameboard()
        game.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      ["red", 0, 0, 0, 0, 0, 0],
                      ["red", "yellow", 0, 0, 0, 0, 0],
                      ["red", "yellow", 0, 0, 0, 0, 0],
                      ["red", "yellow", 0, 0, 0, 0, 0]]
        game.player1 = "red"
        self.assertEqual(game.isWinner("p1"), True)
        self.assertEqual(game.isWinner("p2"), False)

    # Checks if the current turn is played by the player who clicked
    def test_players_turn(self):
        game = Gameboard()
        game.current_turn = 'p1'
        self.assertEqual(game.players_turn("p1"), True)
        self.assertEqual(game.players_turn("p2"), False)

    # Checks if it is a draw
    def test_isDraw(self):
        game = Gameboard()
        game.remaining_moves = 0
        self.assertEqual(game.isDraw(), True)
        game.remaining_moves = 1
        self.assertEqual(game.isDraw(), False)

    # Checks if there is space left in the column clicked
    def test_isCurrentColumnFilled(self):
        game = Gameboard()
        game.positions[0] = -1
        game.positions[1] = 1
        self.assertEqual(game.isCurrentColumnFilled(0), True)
        self.assertEqual(game.isCurrentColumnFilled(1), False)

    # Updates the board and switches the current turn to other player
    def test_happyMove(self):
        game = Gameboard()
        player_name = 'p1'
        game.positions = [5]*7
        pos = 0
        self.assertEqual(game.happyMove(player_name, pos), True)
        player_name = 'p2'
        self.assertEqual(game.happyMove(player_name, pos), True)


if __name__ == '__main__':
    unittest.main()
