import unittest
import db


class Test_Testdb(unittest.TestCase):

    # test whether a given move was added to DB
    def test_add_move(self):
        db.clear()
        db.init_db()
        board = [[0 for x in range(7)] for y in range(6)]
        move = ['', str(board), '',
                'red', 'yellow', 40]
        self.assertEqual(db.add_move(move), True)

    # test whether we get the right move from DB
    def test_get_move(self):
        board = [[0 for x in range(7)] for y in range(6)]
        move = ['', str(board), '',
                'red', 'yellow', 40]
        self.assertEqual(db.getMove(), tuple(move))
