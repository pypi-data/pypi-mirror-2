import math
import unittest

from pyeigen import Matrix4f

from settings import TEST_PRECISION

 
class TestMatrix4fCreate(unittest.TestCase):
    def test_constructor_default(self):
        m = Matrix4f()
        for i in range(4):
            for j in range(4):
                self.assertEqual(m[i, j], 0)

    def test_constructor_arguments(self):
        m = Matrix4f(1, 2, 3, 4,
                     5, 6, 7, 8,
                     9, 10, 11, 12,
                     13, 14, 15, 16)
        self.assertEqual(m[0, 0], 1)
        self.assertEqual(m[0, 1], 2)
        self.assertEqual(m[0, 2], 3)
        self.assertEqual(m[0, 3], 4)
        self.assertEqual(m[1, 0], 5)
        self.assertEqual(m[1, 1], 6)
        self.assertEqual(m[1, 2], 7)
        self.assertEqual(m[1, 3], 8)
        self.assertEqual(m[2, 0], 9)
        self.assertEqual(m[2, 1], 10)
        self.assertEqual(m[2, 2], 11)
        self.assertEqual(m[2, 3], 12)
        self.assertEqual(m[3, 0], 13)
        self.assertEqual(m[3, 1], 14)
        self.assertEqual(m[3, 2], 15)
        self.assertEqual(m[3, 3], 16)

    def test_zero(self):
        m = Matrix4f.zero()
        for i in range(4):
            for j in range(4):
                self.assertEqual(m[i, j], 0)

    def test_ones(self):
        m = Matrix4f.ones()
        for i in range(4):
            for j in range(4):
                self.assertEqual(m[i, j], 1)

    def test_constant(self):
        m = Matrix4f.constant(2)
        for i in range(4):
            for j in range(4):
                self.assertEqual(m[i, j], 2)

    def test_identity(self):
        m = Matrix4f.identity()
        for i in range(4):
            for j in range(4):
                if i == j:
                    self.assertEqual(m[i, j], 1)
                else:
                    self.assertEqual(m[i, j], 0)

    def test_random(self):
        m = Matrix4f.random()
        for i in range(4):
            for j in range(4):
                self.assert_(m[i, j] > -1)
                self.assert_(m[i, j] < 1)

class TestMatrix4f(unittest.TestCase):
    def setUp(self):
        self.m1 = Matrix4f(-1, -2, -3, -4,
                           -5, -6, -7, -8,
                           -9, -10, -11, -12,
                           -13, -14, -15, -16)
        self.m2 = Matrix4f(-16, -15, -14, -13,
                           -12, -11, -10, -9,
                           -8, -7, -6, -5,
                           -4, -3, -2, -1)

    def test_set(self):
        self.m1.set(1, 2, 3, 4,
                    5, 6, 7, 8,
                    9, 10, 11, 12,
                    13, 14, 15, 16)
        self.assertEqual(self.m1[0, 0], 1)
        self.assertEqual(self.m1[0, 1], 2)
        self.assertEqual(self.m1[0, 2], 3)
        self.assertEqual(self.m1[0, 3], 4)
        self.assertEqual(self.m1[1, 0], 5)
        self.assertEqual(self.m1[1, 1], 6)
        self.assertEqual(self.m1[1, 2], 7)
        self.assertEqual(self.m1[1, 3], 8)
        self.assertEqual(self.m1[2, 0], 9)
        self.assertEqual(self.m1[2, 1], 10)
        self.assertEqual(self.m1[2, 2], 11)
        self.assertEqual(self.m1[2, 3], 12)
        self.assertEqual(self.m1[3, 0], 13)
        self.assertEqual(self.m1[3, 1], 14)
        self.assertEqual(self.m1[3, 2], 15)
        self.assertEqual(self.m1[3, 3], 16)

    def test_set_zero(self):
        self.m1.set_zero()
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.m1[i, j], 0)
    
    def test_set_ones(self):
        self.m1.set_ones()
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.m1[i, j], 1)
    
    def test_set_constant(self):
        self.m1.set_constant(2)
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.m1[i, j], 2)
    
    def test_set_random(self):
        self.m1.set_random()
        for i in range(4):
            for j in range(4):
                self.assert_(self.m1[i, j] > -1)
                self.assert_(self.m1[i, j] < 1)
    
    def test_inverse(self):
        identity = Matrix4f.identity()
        inverse = identity.inverse
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(identity[i, j], inverse[i, j],
                                       TEST_PRECISION)

        random = Matrix4f.random()
        multiplied = random * random.inverse
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(identity[i, j], multiplied[i, j],
                                       TEST_PRECISION)

        multiplied = random.inverse * random
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(identity[i, j], multiplied[i, j],
                                       TEST_PRECISION)

    def test_transpose(self):
        rm1 = self.m1.transpose
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.m1[i, j], rm1[j, i])

    def test_add(self):
        m3 = self.m1 + self.m2
        for i in range(4):
            for j in range(4):
                self.assertEqual(m3[i, j], -17)
        
    def test_sub(self):
        m3 = self.m1 - self.m2
        self.assertEqual(m3[0, 0], 15)
        self.assertEqual(m3[0, 1], 13)
        self.assertEqual(m3[0, 2], 11)
        self.assertEqual(m3[0, 3], 9)
        self.assertEqual(m3[1, 0], 7)
        self.assertEqual(m3[1, 1], 5)
        self.assertEqual(m3[1, 2], 3)
        self.assertEqual(m3[1, 3], 1)
        self.assertEqual(m3[2, 0], -1)
        self.assertEqual(m3[2, 1], -3)
        self.assertEqual(m3[2, 2], -5)
        self.assertEqual(m3[2, 3], -7)
        self.assertEqual(m3[3, 0], -9)
        self.assertEqual(m3[3, 1], -11)
        self.assertEqual(m3[3, 2], -13)
        self.assertEqual(m3[3, 3], -15)

    def test_mul_scalar(self):
        m3 = self.m1 * 2
        for i in range(4):
            for j in range(4):
                self.assertEqual(m3[i, j], self.m1[i, j] * 2)

    def test_div(self):
        m3 = self.m1 / 2
        for i in range(4):
            for j in range(4):
                self.assertEqual(m3[i, j], self.m1[i, j] / 2)

    def test_negative(self):
        m3 = -self.m1
        for i in range(4):
            for j in range(4):
                self.assertEqual(m3[i, j], -self.m1[i, j])
        m4 = -m3
        for i in range(4):
            for j in range(4):
                self.assertEqual(m4[i, j], self.m1[i, j])

    def test_inplace_add(self):
        self.m1 += self.m2
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.m1[i, j], -17)

    def test_inplace_sub(self):
        self.m1 -= self.m2
        self.assertEqual(self.m1[0, 0], 15)
        self.assertEqual(self.m1[0, 1], 13)
        self.assertEqual(self.m1[0, 2], 11)
        self.assertEqual(self.m1[0, 3], 9)
        self.assertEqual(self.m1[1, 0], 7)
        self.assertEqual(self.m1[1, 1], 5)
        self.assertEqual(self.m1[1, 2], 3)
        self.assertEqual(self.m1[1, 3], 1)
        self.assertEqual(self.m1[2, 0], -1)
        self.assertEqual(self.m1[2, 1], -3)
        self.assertEqual(self.m1[2, 2], -5)
        self.assertEqual(self.m1[2, 3], -7)
        self.assertEqual(self.m1[3, 0], -9)
        self.assertEqual(self.m1[3, 1], -11)
        self.assertEqual(self.m1[3, 2], -13)
        self.assertEqual(self.m1[3, 3], -15)

    def test_inplace_mul_scalar(self):
        self.m1 *= 2
        self.assertEqual(self.m1[0, 0], -2)
        self.assertEqual(self.m1[0, 1], -4)
        self.assertEqual(self.m1[0, 2], -6)
        self.assertEqual(self.m1[0, 3], -8)
        self.assertEqual(self.m1[1, 0], -10)
        self.assertEqual(self.m1[1, 1], -12)
        self.assertEqual(self.m1[1, 2], -14)
        self.assertEqual(self.m1[1, 3], -16)
        self.assertEqual(self.m1[2, 0], -18)
        self.assertEqual(self.m1[2, 1], -20)
        self.assertEqual(self.m1[2, 2], -22)
        self.assertEqual(self.m1[2, 3], -24)
        self.assertEqual(self.m1[3, 0], -26)
        self.assertEqual(self.m1[3, 1], -28)
        self.assertEqual(self.m1[3, 2], -30)
        self.assertEqual(self.m1[3, 3], -32)

    def test_inplace_div(self):
        self.m1 /= 2
        self.assertEqual(self.m1[0, 0], -0.5)
        self.assertEqual(self.m1[0, 1], -1)
        self.assertEqual(self.m1[0, 2], -1.5)
        self.assertEqual(self.m1[0, 3], -2)
        self.assertEqual(self.m1[1, 0], -2.5)
        self.assertEqual(self.m1[1, 1], -3)
        self.assertEqual(self.m1[1, 2], -3.5)
        self.assertEqual(self.m1[1, 3], -4)
        self.assertEqual(self.m1[2, 0], -4.5)
        self.assertEqual(self.m1[2, 1], -5)
        self.assertEqual(self.m1[2, 2], -5.5)
        self.assertEqual(self.m1[2, 3], -6)
        self.assertEqual(self.m1[3, 0], -6.5)
        self.assertEqual(self.m1[3, 1], -7)
        self.assertEqual(self.m1[3, 2], -7.5)
        self.assertEqual(self.m1[3, 3], -8)

    def test_len(self):
        self.assertEqual(len(self.m1), 16)

    def test_item(self):
        self.m1[0, 0] = 1
        self.m1[0, 1] = 2
        self.m1[0, 2] = 3
        self.m1[0, 3] = 4
        self.m1[1, 0] = 5
        self.m1[1, 1] = 6
        self.m1[1, 2] = 7
        self.m1[1, 3] = 8
        self.m1[2, 0] = 9
        self.m1[2, 1] = 10
        self.m1[2, 2] = 11
        self.m1[2, 3] = 12
        self.m1[3, 0] = 13
        self.m1[3, 1] = 14
        self.m1[3, 2] = 15
        self.m1[3, 3] = 16
        self.assertEqual(self.m1[0, 0], 1)
        self.assertEqual(self.m1[0, 1], 2)
        self.assertEqual(self.m1[0, 2], 3)
        self.assertEqual(self.m1[0, 3], 4)
        self.assertEqual(self.m1[1, 0], 5)
        self.assertEqual(self.m1[1, 1], 6)
        self.assertEqual(self.m1[1, 2], 7)
        self.assertEqual(self.m1[1, 3], 8)
        self.assertEqual(self.m1[2, 0], 9)
        self.assertEqual(self.m1[2, 1], 10)
        self.assertEqual(self.m1[2, 2], 11)
        self.assertEqual(self.m1[2, 3], 12)
        self.assertEqual(self.m1[3, 0], 13)
        self.assertEqual(self.m1[3, 1], 14)
        self.assertEqual(self.m1[3, 2], 15)
        self.assertEqual(self.m1[3, 3], 16)

    def test_eq(self):
        self.assert_(self.m1 == self.m1)
        self.assertFalse(self.m1 == self.m2)
        
    def test_ne(self):
        self.assertFalse(self.m1 != self.m1)
        self.assert_(self.m1 != self.m2)
        
if __name__ == '__main__':
    unittest.main()
