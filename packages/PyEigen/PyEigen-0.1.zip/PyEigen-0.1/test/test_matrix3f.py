import math
import unittest

from pyeigen import Matrix3f

from settings import TEST_PRECISION

 
class TestMatrix3fCreate(unittest.TestCase):
    def test_constructor_default(self):
        m = Matrix3f()
        for i in range(3):
            for j in range(3):
                self.assertEqual(m[i, j], 0)

    def test_constructor_arguments(self):
        m = Matrix3f(1, 2, 3,
                     4, 5, 6,
                     7, 8, 9)
        self.assertEqual(m[0, 0], 1)
        self.assertEqual(m[0, 1], 2)
        self.assertEqual(m[0, 2], 3)
        self.assertEqual(m[1, 0], 4)
        self.assertEqual(m[1, 1], 5)
        self.assertEqual(m[1, 2], 6)
        self.assertEqual(m[2, 0], 7)
        self.assertEqual(m[2, 1], 8)
        self.assertEqual(m[2, 2], 9)

    def test_zero(self):
        m = Matrix3f.zero()
        for i in range(3):
            for j in range(3):
                self.assertEqual(m[i, j], 0)

    def test_ones(self):
        m = Matrix3f.ones()
        for i in range(3):
            for j in range(3):
                self.assertEqual(m[i, j], 1)

    def test_constant(self):
        m = Matrix3f.constant(2)
        for i in range(3):
            for j in range(3):
                self.assertEqual(m[i, j], 2)

    def test_identity(self):
        m = Matrix3f.identity()
        for i in range(3):
            for j in range(3):
                if i == j:
                    self.assertEqual(m[i, j], 1)
                else:
                    self.assertEqual(m[i, j], 0)

    def test_random(self):
        m = Matrix3f.random()
        for i in range(3):
            for j in range(3):
                self.assert_(m[i, j] > -1)
                self.assert_(m[i, j] < 1)

class TestMatrix3f(unittest.TestCase):
    def setUp(self):
        self.m1 = Matrix3f(-1, -2, -3,
                           -4, -5, -6,
                           -7, -8, -9)
        self.m2 = Matrix3f(-9, -8, -7,
                           -6, -5, -4,
                           -3, -2, -1)

    def test_set(self):
        self.m1.set(1, 2, 3,
                    4, 5, 6,
                    7, 8, 9)
        self.assertEqual(self.m1[0, 0], 1)
        self.assertEqual(self.m1[0, 1], 2)
        self.assertEqual(self.m1[0, 2], 3)
        self.assertEqual(self.m1[1, 0], 4)
        self.assertEqual(self.m1[1, 1], 5)
        self.assertEqual(self.m1[1, 2], 6)
        self.assertEqual(self.m1[2, 0], 7)
        self.assertEqual(self.m1[2, 1], 8)
        self.assertEqual(self.m1[2, 2], 9)

    def test_set_zero(self):
        self.m1.set_zero()
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.m1[i, j], 0)
    
    def test_set_ones(self):
        self.m1.set_ones()
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.m1[i, j], 1)
    
    def test_set_constant(self):
        self.m1.set_constant(2)
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.m1[i, j], 2)
    
    def test_set_random(self):
        self.m1.set_random()
        for i in range(3):
            for j in range(3):
                self.assert_(self.m1[i, j] > -1)
                self.assert_(self.m1[i, j] < 1)
    
    def test_inverse(self):
        identity = Matrix3f.identity()
        inverse = identity.inverse
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(identity[i, j], inverse[i, j],
                                       TEST_PRECISION)

        random = Matrix3f.random()
        multiplied = random * random.inverse
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(identity[i, j], multiplied[i, j],
                                       TEST_PRECISION)

        multiplied = random.inverse * random
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(identity[i, j], multiplied[i, j],
                                       TEST_PRECISION)

    def test_transpose(self):
        rm1 = self.m1.transpose
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.m1[i, j], rm1[j, i])

    def test_add(self):
        m3 = self.m1 + self.m2
        for i in range(3):
            for j in range(3):
                self.assertEqual(m3[i, j], -10)
        
    def test_sub(self):
        m3 = self.m1 - self.m2
        self.assertEqual(m3[0, 0], 8)
        self.assertEqual(m3[0, 1], 6)
        self.assertEqual(m3[0, 2], 4)
        self.assertEqual(m3[1, 0], 2)
        self.assertEqual(m3[1, 1], 0)
        self.assertEqual(m3[1, 2], -2)
        self.assertEqual(m3[2, 0], -4)
        self.assertEqual(m3[2, 1], -6)
        self.assertEqual(m3[2, 2], -8)

    def test_mul_scalar(self):
        m3 = self.m1 * 2
        for i in range(3):
            for j in range(3):
                self.assertEqual(m3[i, j], self.m1[i, j] * 2)

    def test_div(self):
        m3 = self.m1 / 2
        for i in range(3):
            for j in range(3):
                self.assertEqual(m3[i, j], self.m1[i, j] / 2)

    def test_negative(self):
        m3 = -self.m1
        for i in range(3):
            for j in range(3):
                self.assertEqual(m3[i, j], -self.m1[i, j])
        m4 = -m3
        for i in range(3):
            for j in range(3):
                self.assertEqual(m4[i, j], self.m1[i, j])

    def test_inplace_add(self):
        self.m1 += self.m2
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.m1[i, j], -10)

    def test_inplace_sub(self):
        self.m1 -= self.m2
        self.assertEqual(self.m1[0, 0], 8)
        self.assertEqual(self.m1[0, 1], 6)
        self.assertEqual(self.m1[0, 2], 4)
        self.assertEqual(self.m1[1, 0], 2)
        self.assertEqual(self.m1[1, 1], 0)
        self.assertEqual(self.m1[1, 2], -2)
        self.assertEqual(self.m1[2, 0], -4)
        self.assertEqual(self.m1[2, 1], -6)
        self.assertEqual(self.m1[2, 2], -8)

    def test_inplace_mul_scalar(self):
        self.m1 *= 2
        self.assertEqual(self.m1[0, 0], -2)
        self.assertEqual(self.m1[0, 1], -4)
        self.assertEqual(self.m1[0, 2], -6)
        self.assertEqual(self.m1[1, 0], -8)
        self.assertEqual(self.m1[1, 1], -10)
        self.assertEqual(self.m1[1, 2], -12)
        self.assertEqual(self.m1[2, 0], -14)
        self.assertEqual(self.m1[2, 1], -16)
        self.assertEqual(self.m1[2, 2], -18)

    def test_inplace_div(self):
        self.m1 /= 2
        self.assertEqual(self.m1[0, 0], -0.5)
        self.assertEqual(self.m1[0, 1], -1)
        self.assertEqual(self.m1[0, 2], -1.5)
        self.assertEqual(self.m1[1, 0], -2)
        self.assertEqual(self.m1[1, 1], -2.5)
        self.assertEqual(self.m1[1, 2], -3)
        self.assertEqual(self.m1[2, 0], -3.5)
        self.assertEqual(self.m1[2, 1], -4)
        self.assertEqual(self.m1[2, 2], -4.5)

    def test_len(self):
        self.assertEqual(len(self.m1), 9)

    def test_item(self):
        self.m1[0, 0] = 1
        self.m1[0, 1] = 2
        self.m1[0, 2] = 3
        self.m1[1, 0] = 4
        self.m1[1, 1] = 5
        self.m1[1, 2] = 6
        self.m1[2, 0] = 7
        self.m1[2, 1] = 8
        self.m1[2, 2] = 9
        self.assertEqual(self.m1[0, 0], 1)
        self.assertEqual(self.m1[0, 1], 2)
        self.assertEqual(self.m1[0, 2], 3)
        self.assertEqual(self.m1[1, 0], 4)
        self.assertEqual(self.m1[1, 1], 5)
        self.assertEqual(self.m1[1, 2], 6)
        self.assertEqual(self.m1[2, 0], 7)
        self.assertEqual(self.m1[2, 1], 8)
        self.assertEqual(self.m1[2, 2], 9)

    def test_eq(self):
        self.assert_(self.m1 == self.m1)
        self.assertFalse(self.m1 == self.m2)
        
    def test_ne(self):
        self.assertFalse(self.m1 != self.m1)
        self.assert_(self.m1 != self.m2)
        
if __name__ == '__main__':
    unittest.main()
