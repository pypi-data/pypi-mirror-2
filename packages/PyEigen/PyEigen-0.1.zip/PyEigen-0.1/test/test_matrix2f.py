import math
import unittest

from pyeigen import Matrix2f

from settings import TEST_PRECISION

 
class TestMatrix2fCreate(unittest.TestCase):
    def test_constructor_default(self):
        m = Matrix2f()
        for i in range(2):
            for j in range(2):
                self.assertEqual(m[i, j], 0)

    def test_constructor_arguments(self):
        m = Matrix2f(1, 2,
                     3, 4)
        self.assertEqual(m[0, 0], 1)
        self.assertEqual(m[0, 1], 2)
        self.assertEqual(m[1, 0], 3)
        self.assertEqual(m[1, 1], 4)

    def test_zero(self):
        m = Matrix2f.zero()
        for i in range(2):
            for j in range(2):
                self.assertEqual(m[i, j], 0)

    def test_ones(self):
        m = Matrix2f.ones()
        for i in range(2):
            for j in range(2):
                self.assertEqual(m[i, j], 1)

    def test_constant(self):
        m = Matrix2f.constant(2)
        for i in range(2):
            for j in range(2):
                self.assertEqual(m[i, j], 2)

    def test_identity(self):
        m = Matrix2f.identity()
        for i in range(2):
            for j in range(2):
                if i == j:
                    self.assertEqual(m[i, j], 1)
                else:
                    self.assertEqual(m[i, j], 0)

    def test_random(self):
        m = Matrix2f.random()
        for i in range(2):
            for j in range(2):
                self.assert_(m[i, j] > -1)
                self.assert_(m[i, j] < 1)

class TestMatrix2f(unittest.TestCase):
    def setUp(self):
        self.m1 = Matrix2f(-1, -2,
                           -3, -4)
        self.m2 = Matrix2f(-5, -6,
                           -7, -8)

    def test_set(self):
        self.m1.set(1, 2,
                    3, 4)
        self.assertEqual(self.m1[0, 0], 1)
        self.assertEqual(self.m1[0, 1], 2)
        self.assertEqual(self.m1[1, 0], 3)
        self.assertEqual(self.m1[1, 1], 4)
    
    def test_set_zero(self):
        self.m1.set_zero()
        for i in range(2):
            for j in range(2):
                self.assertEqual(self.m1[i, j], 0)
    
    def test_set_ones(self):
        self.m1.set_ones()
        for i in range(2):
            for j in range(2):
                self.assertEqual(self.m1[i, j], 1)
    
    def test_set_constant(self):
        self.m1.set_constant(2)
        for i in range(2):
            for j in range(2):
                self.assertEqual(self.m1[i, j], 2)
    
    def test_set_random(self):
        self.m1.set_random()
        for i in range(2):
            for j in range(2):
                self.assert_(self.m1[i, j] > -1)
                self.assert_(self.m1[i, j] < 1)
    
    def test_inverse(self):
        identity = Matrix2f.identity()
        inverse = identity.inverse
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(identity[i, j], inverse[i, j],
                                       TEST_PRECISION)

        random = Matrix2f.random()
        multiplied = random * random.inverse
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(identity[i, j], multiplied[i, j],
                                       TEST_PRECISION)

        multiplied = random.inverse * random
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(identity[i, j], multiplied[i, j],
                                       TEST_PRECISION)

    def test_transpose(self):
        rm1 = self.m1.transpose
        self.assertEqual(self.m1[0, 0], rm1[0, 0])
        self.assertEqual(self.m1[0, 1], rm1[1, 0])
        self.assertEqual(self.m1[1, 0], rm1[0, 1])
        self.assertEqual(self.m1[1, 1], rm1[1, 1])

    def test_add(self):
        m3 = self.m1 + self.m2
        self.assertEqual(m3[0, 0], -6)
        self.assertEqual(m3[0, 1], -8)
        self.assertEqual(m3[1, 0], -10)
        self.assertEqual(m3[1, 1], -12)
        
    def test_sub(self):
        m3 = self.m1 - self.m2
        self.assertEqual(m3[0, 0], 4)
        self.assertEqual(m3[0, 1], 4)
        self.assertEqual(m3[1, 0], 4)
        self.assertEqual(m3[1, 1], 4)

    def test_mul_scalar(self):
        m3 = self.m1 * 2
        self.assertEqual(m3[0, 0], -2)
        self.assertEqual(m3[0, 1], -4)
        self.assertEqual(m3[1, 0], -6)
        self.assertEqual(m3[1, 1], -8)

    def test_div(self):
        m3 = self.m1 / 2
        self.assertEqual(m3[0, 0], -0.5)
        self.assertEqual(m3[0, 1], -1)
        self.assertEqual(m3[1, 0], -1.5)
        self.assertEqual(m3[1, 1], -2)

    def test_negative(self):
        m3 = -self.m1
        self.assertEqual(m3[0, 0], 1)
        self.assertEqual(m3[0, 1], 2)
        self.assertEqual(m3[1, 0], 3)
        self.assertEqual(m3[1, 1], 4)
        m4 = -m3
        self.assertEqual(m4[0, 0], -1)
        self.assertEqual(m4[0, 1], -2)
        self.assertEqual(m4[1, 0], -3)
        self.assertEqual(m4[1, 1], -4)

    def test_inplace_add(self):
        self.m1 += self.m2
        self.assertEqual(self.m1[0, 0], -6)
        self.assertEqual(self.m1[0, 1], -8)
        self.assertEqual(self.m1[1, 0], -10)
        self.assertEqual(self.m1[1, 1], -12)
        
    def test_inplace_sub(self):
        self.m1 -= self.m2
        self.assertEqual(self.m1[0, 0], 4)
        self.assertEqual(self.m1[0, 1], 4)
        self.assertEqual(self.m1[1, 0], 4)
        self.assertEqual(self.m1[1, 1], 4)

    def test_inplace_mul_scalar(self):
        self.m1 *= 2
        self.assertEqual(self.m1[0, 0], -2)
        self.assertEqual(self.m1[0, 1], -4)
        self.assertEqual(self.m1[1, 0], -6)
        self.assertEqual(self.m1[1, 1], -8)

    def test_inplace_div(self):
        self.m1 /= 2
        self.assertEqual(self.m1[0, 0], -0.5)
        self.assertEqual(self.m1[0, 1], -1)
        self.assertEqual(self.m1[1, 0], -1.5)
        self.assertEqual(self.m1[1, 1], -2)

    def test_len(self):
        self.assertEqual(len(self.m1), 4)

    def test_item(self):
        self.m1[0, 0] = 1
        self.m1[0, 1] = 2
        self.m1[1, 0] = 3
        self.m1[1, 1] = 4
        self.assertEqual(self.m1[0, 0], 1)
        self.assertEqual(self.m1[0, 1], 2)
        self.assertEqual(self.m1[1, 0], 3)
        self.assertEqual(self.m1[1, 1], 4)

    def test_eq(self):
        self.assert_(self.m1 == self.m1)
        self.assertFalse(self.m1 == self.m2)
        
    def test_ne(self):
        self.assertFalse(self.m1 != self.m1)
        self.assert_(self.m1 != self.m2)
        
if __name__ == '__main__':
    unittest.main()
