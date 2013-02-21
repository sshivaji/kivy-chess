import unittest

import sys; sys.path.extend(['../', './'])
from square import Square
import chess

class TestSquare(unittest.TestCase):
	def test___eq__(self):
		square = Square("a1")
		same = Square("a1")
		other = Square("a2")
		
		self.assertEqual(True, square.__eq__(same))
		self.assertEqual(False, square.__eq__(other))

	def test___hash__(self):
		d = {}
		for square in Square.get_all():
			d[hash(square)] = None
		total = len(Square.ranks) * len(Square.files)
		self.assertEqual(total, len(d))

	def test___init__(self):
		for r, f in zip(Square.ranks , Square.files):
			square = Square(f + r)

	def test___ne__(self):
		square = Square("a1")
		same = Square("a1")
		other = Square("a2")
		
		self.assertEqual(False , square.__ne__(same))
		self.assertEqual(True, square.__ne__(other))

	def test___repr__(self):
		square = Square("a1")
		self.assertEqual("Square('a1')", square.__repr__())

	def test___str__(self):
		square = Square("a1")
		self.assertEqual('a1', square.__str__())

	def test_file(self):
		square = Square("a1")
		self.assertEqual('a', square.file)

	def test_from_rank_and_file(self):
		square = Square.from_rank_and_file('1', 'a')
		self.assertEqual('a1', str(square))

	def test_from_x88(self):
		square = Square.from_x88(0)
		self.assertEqual('a1', str(square))

	def test_from_x_and_y(self):
		square = Square.from_x_and_y(0, 0 )
		self.assertEqual('a1', str(square))

	def test_get_all(self):
		for idx, square in enumerate(Square.get_all()):
			pass
		total = len(Square.ranks) * len(Square.files)
		self.assertEqual(total - 1, idx)

	def test_index(self):
		square = Square("a1")
		self.assertEqual(0, square.index)

	def test_is_backrank(self):
		square = Square("a1")
		self.assertEqual(True, square.is_backrank())

	def test_is_dark(self):
		square = Square("a1")
		self.assertEqual(True, square.is_dark())

	def test_is_light(self):
		square = Square("a1")
		self.assertEqual(False, square.is_light())

	def test_name(self):
		square = Square("a1")
		self.assertEqual('a1', square.name)

	def test_rank(self):
		square = Square("a1")
		self.assertEqual('1', square.rank)

	def test_x(self):
		square = Square("a1")
		self.assertEqual(0, square.x)

	def test_x88(self):
		square = Square("a1")
		self.assertEqual(0, square.x88)

	def test_y(self):
		square = Square("a1")
		self.assertEqual(0, square.y)


	# orignal tests
	def test_equality(self):
		"""Tests the overriden equality behaviour of the Square class."""
		a = chess.Square("b4")
		b = chess.Square("b4")
		c = chess.Square("b3")
		d = chess.Square("f3")

		self.assertEqual(a, b)
		self.assertEqual(b, a)

		self.assertNotEqual(a, c)
		self.assertNotEqual(a, d)
		self.assertNotEqual(c, d)

	def test_simple_properties(self):
		"""Tests simple properties of Square objects."""
		f7 = chess.Square("f7")
		self.assertFalse(f7.is_dark())
		self.assertTrue(f7.is_light())

		#XXX rank changed to return string
		self.assertEqual(f7.rank, '7')

		self.assertEqual(f7.file, 'f')
		self.assertEqual(f7.name, 'f7')

		
		# XXX joy joy I have enidaness has changed
		#self.assertEqual(f7.x88, 21)

		self.assertEqual(f7.x, 5)
		self.assertEqual(f7.y, 6)
		self.assertFalse(f7.is_backrank())

	def test_creation(self):
		"""Tests creation of Square instances."""
		self.assertEqual(chess.Square.from_x_and_y(3, 5), chess.Square("d6"))

		# endian issue
		#self.assertEqual(chess.Square.from_x88(2), chess.Square("c8"))

		self.assertEqual(chess.Square.from_x88(2), chess.Square("c1"))

		self.assertEqual(chess.Square.from_rank_and_file(rank=2, file="g"), chess.Square("g2"))

	def test_iteration(self):
		"""Tests iteration over all squares."""
		self.assertTrue(chess.Square("h8") in chess.Square.get_all())
		self.assertTrue(chess.Square("b1") in chess.Square.get_all())

if __name__ == '__main__':
	unittest.main()
