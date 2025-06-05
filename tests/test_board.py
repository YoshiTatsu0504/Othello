import unittest

from src.board import Board, BLACK, WHITE, EMPTY


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_initial_setup(self):
        black = self.board.count(BLACK)
        white = self.board.count(WHITE)
        self.assertEqual(black, 2)
        self.assertEqual(white, 2)

    def test_valid_move(self):
        self.assertTrue(self.board.is_valid_move(BLACK, 2, 3))
        self.assertTrue(self.board.is_valid_move(WHITE, 2, 4))
        self.assertFalse(self.board.is_valid_move(BLACK, 0, 0))

    def test_apply_move(self):
        self.assertTrue(self.board.apply_move(BLACK, 2, 3))
        self.assertEqual(self.board.get(2, 3), BLACK)
        self.assertEqual(self.board.get(3, 3), BLACK)
        self.assertEqual(self.board.count(BLACK), 4)

    def test_no_move_on_filled(self):
        self.assertTrue(self.board.apply_move(BLACK, 2, 3))
        self.assertFalse(self.board.apply_move(WHITE, 2, 3))

    def test_full_board_detection(self):
        # Fill board artificially
        for y in range(8):
            for x in range(8):
                self.board.set(x, y, BLACK)
        self.assertTrue(self.board.is_full())


if __name__ == '__main__':
    unittest.main()
