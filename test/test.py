import unittest
import math
import random
from src.util.point import Point
from src.core.translate import Translator
from src.core.parse import Parser
from src.util.amino import Amino


class TestPoint(unittest.TestCase):
    def test_add(self):
        p = Point(1, 2, 3) + Point(2, 4, 6)
        self.assertEqual(p, Point(3, 6, 9))
        p = Point(1, 2, 3) + 2
        self.assertEqual(p, Point(3, 4, 5))
        p = Point(1, 2, 3)
        p += Point(2, 4, 6)
        self.assertEqual(p, Point(3, 6, 9))
        p = Point(1, 2, 3)
        p += 2
        self.assertEqual(p, Point(3, 4, 5))

    def test_sub(self):
        p = Point(1, 2, 3) - Point(2, 4, 6)
        self.assertEqual(p, Point(-1, -2, -3))
        p = Point(1, 2, 3) - 2
        self.assertEqual(p, Point(-1, 0, 1))
        p = Point(1, 2, 3)
        p -= Point(2, 4, 6)
        self.assertEqual(p, Point(-1, -2, -3))
        p = Point(1, 2, 3)
        p -= 2
        self.assertEqual(p, Point(-1, 0, 1))

    def test_mul(self):
        p = Point(1, 2, 3) * Point(2, 4, 6)
        self.assertEqual(p, Point(2, 8, 18))
        p = Point(1, 2, 3) * 2
        self.assertEqual(p, Point(2, 4, 6))
        p = Point(1, 2, 3)
        p *= Point(2, 4, 6)
        self.assertEqual(p, Point(2, 8, 18))
        p = Point(1, 2, 3)
        p *= 2
        self.assertEqual(p, Point(2, 4, 6))

    def test_div(self):
        p = Point(1, 2, 3) / Point(2, 4, 6)
        self.assertEqual(p, Point(0.5, 0.5, 0.5))
        p = Point(1, 2, 3) / 2
        self.assertEqual(p, Point(0.5, 1, 1.5))
        p = Point(1, 2, 3)
        p /= Point(2, 4, 6)
        self.assertEqual(p, Point(0.5, 0.5, 0.5))
        p = Point(1, 2, 3)
        p /= 2
        self.assertEqual(p, Point(0.5, 1, 1.5))

    def test_dot(self):
        d = Point(1, 2, 3) | Point(4, 6, 2)
        self.assertEqual(d, 22)

    def test_cross(self):
        p = Point(1, 2, 3) ^ Point(4, 6, 2)
        self.assertEqual(p, Point(-14, 10, -2))
        p = Point(1, 2, 3)
        p ^= Point(4, 6, 2)
        self.assertEqual(p, Point(-14, 10, -2))

    def test_neg(self):
        p = Point(1, 2, 3)
        self.assertEqual(-p, Point(-1, -2, -3))

    def test_len(self):
        p = Point(1, 2, 3)
        self.assertEqual(p.lensq(), 14)
        self.assertAlmostEqual(p.length(), 3.74165738)

    def test_norm(self):
        p = Point(3, 4, 0)
        self.assertEqual(~p, Point(0.6, 0.8, 0))
        p.norm()
        self.assertEqual(p, Point(0.6, 0.8, 0))

    def test_rotate(self):
        p = Point(1, 2, 3)
        self.assertEqual(p.rotated(Point(1, 0, 0), 0), Point(1, 2, 3))
        self.assertEqual(
            p.rotated(Point(1, 0, 0), math.pi / 2).rounded(5), Point(1, -3, 2))
        self.assertEqual(
            p.rotated(Point(1, 0, 0), -math.pi / 2).rounded(5), Point(
                1, 3, -2))


class TestTranslator(unittest.TestCase):
    def test_forward_backward(self):
        points = []
        for i in range(0, 10):
            points.append(
                Point(random.random() * 20 - 10,
                      random.random() * 20 - 10,
                      random.random() * 20 - 10))
        trans = Translator()
        polars = trans.forward(points)
        trans = Translator()
        original = trans.backward(polars)
        for i in range(0, 10):
            self.assertEqual(points[i].rounded(5), original[i].rounded(5))


class TestParser(unittest.TestCase):
    def test_read_file(self):
        aminos = Parser().read_file('test/test.pdb')
        self.assertEqual(len(aminos), 3)
        self.assertEqual(aminos[0].type, 'PRO')
        self.assertEqual(aminos[0].N, Point(-69.116000, 7.943000, -16.525000))
        self.assertEqual(aminos[0].CA, Point(-70.302000, 8.654000, -17.017000))
        self.assertEqual(aminos[0].C, Point(-71.449000, 7.711000, -17.377000))


class TestAmino(unittest.TestCase):
    def test_lookup_code(self):
        self.assertEqual(Amino.lookup_code(None), None)
        self.assertEqual(Amino.lookup_code(''), None)
        self.assertEqual(Amino.lookup_code('A'), 'ALA')
        self.assertEqual(Amino.lookup_code('a'), 'ALA')
        self.assertEqual(Amino.lookup_code('B'), None)
        self.assertEqual(Amino.lookup_code('Alanine'), 'ALA')
        self.assertEqual(Amino.lookup_code('aLanine'), 'ALA')
        self.assertEqual(Amino.lookup_code('ala'), 'ALA')
        self.assertEqual(Amino.lookup_code('ALA'), 'ALA')


if __name__ == '__main__':
    unittest.main()
