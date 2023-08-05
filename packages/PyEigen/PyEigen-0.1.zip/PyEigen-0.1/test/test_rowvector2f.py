import math
import unittest

from pyeigen import RowVector2f, Vector2f

from settings import TEST_PRECISION

 
class TestRowVector2fCreate(unittest.TestCase):
    def test_constructor_default(self):
        v = RowVector2f()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)

    def test_constructor_arguments(self):
        v = RowVector2f(1, 2)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)

    def test_zero(self):
        v = RowVector2f.zero()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)

    def test_ones(self):
        v = RowVector2f.ones()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 1)

    def test_constant(self):
        v = RowVector2f.constant(2)
        self.assertEqual(v.x, 2)
        self.assertEqual(v.y, 2)

    def test_random(self):
        v = RowVector2f.random()
        self.assert_(v.x > -1)
        self.assert_(v.x < 1)
        self.assert_(v.y > -1)
        self.assert_(v.y < 1)

    def test_unit_x(self):
        v = RowVector2f.unit_x()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 0)

    def test_unit_y(self):
        v = RowVector2f.unit_y()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 1)

class TestRowVector2f(unittest.TestCase):
    def setUp(self):
        self.v1 = RowVector2f(-1, -2)
        self.v2 = RowVector2f(-3, -4)

    def test_set(self):
        self.v1.set(1, 2)
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
    
    def test_set_zero(self):
        self.v1.set_zero()
        self.assertEqual(self.v1.x, 0)
        self.assertEqual(self.v1.y, 0)
    
    def test_set_ones(self):
        self.v1.set_ones()
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 1)
    
    def test_set_constant(self):
        self.v1.set_constant(2)
        self.assertEqual(self.v1.x, 2)
        self.assertEqual(self.v1.y, 2)
    
    def test_set_random(self):
        self.v1.set_random()
        self.assert_(self.v1.x > -1)
        self.assert_(self.v1.x < 1)
        self.assert_(self.v1.y > -1)
        self.assert_(self.v1.y < 1)

    def test_norm(self):
        v = RowVector2f(1, 0)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = RowVector2f(0, 1)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = RowVector2f(1, 1)
        self.assertAlmostEqual(v.norm, math.sqrt(2), TEST_PRECISION)

    def test_norm_sq(self):
        v = RowVector2f(1, 0)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = RowVector2f(0, 1)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = RowVector2f(1, 1)
        self.assertAlmostEqual(v.norm_sq, 2, TEST_PRECISION)

    def test_normalized(self):
        self.assertAlmostEqual(self.v1.normalized.norm, 1.0, TEST_PRECISION)
        self.assertAlmostEqual(self.v2.normalized.norm, 1.0, TEST_PRECISION)

    def test_transpose(self):
        rv1 = self.v1.transpose
        self.assertEqual(self.v1.x, rv1.x)
        self.assertEqual(self.v1.y, rv1.y)

        self.v1.transpose = Vector2f(1, 2)
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)

    def test_normalize(self):
        self.v1.normalize()
        self.v2.normalize()
        self.assertAlmostEqual(self.v1.norm, 1.0, TEST_PRECISION)
        self.assertAlmostEqual(self.v2.norm, 1.0, TEST_PRECISION)

    def test_add(self):
        v3 = self.v1 + self.v2
        self.assertEqual(v3.x, -4)
        self.assertEqual(v3.y, -6)
        
    def test_sub(self):
        v3 = self.v1 - self.v2
        self.assertEqual(v3.x, 2)
        self.assertEqual(v3.y, 2)

    def test_mul(self):
        v3 = self.v1 * 2
        self.assertEqual(v3.x, -2)
        self.assertEqual(v3.y, -4)

    def test_div(self):
        v3 = self.v1 / 2
        self.assertEqual(v3.x, -0.5)
        self.assertEqual(v3.y, -1)

    def test_negative(self):
        v3 = -self.v1
        self.assertEqual(v3.x, 1)
        self.assertEqual(v3.y, 2)
        v4 = -v3
        self.assertEqual(v4.x, -1)
        self.assertEqual(v4.y, -2)

    def test_inplace_add(self):
        self.v1 += self.v2
        self.assertEqual(self.v1.x, -4)
        self.assertEqual(self.v1.y, -6)
        
    def test_inplace_sub(self):
        self.v1 -= self.v2
        self.assertEqual(self.v1.x, 2)
        self.assertEqual(self.v1.y, 2)

    def test_inplace_mul(self):
        self.v1 *= 2
        self.assertEqual(self.v1.x, -2)
        self.assertEqual(self.v1.y, -4)

    def test_inplace_div(self):
        self.v1 /= 2
        self.assertEqual(self.v1.x, -0.5)
        self.assertEqual(self.v1.y, -1)

    def test_len(self):
        self.assertEqual(len(self.v1), 2)

    def test_get_item(self):
        self.assertEqual(self.v1[0], self.v1.x)
        self.assertEqual(self.v1[1], self.v1.y)

    def test_get_slice(self):
        x, y = self.v1[:]
        self.assertEqual(x, self.v1.x)
        self.assertEqual(y, self.v1.y)

    def test_set_item(self):
        self.v1.x = 1
        self.v1.y = 2
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        
    def test_set_slice(self):
        self.v1[:] = 1, 2
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)

    def test_eq(self):
        self.assert_(self.v1 == self.v1)
        self.assertFalse(self.v1 == self.v2)
        
    def test_ne(self):
        self.assertFalse(self.v1 != self.v1)
        self.assert_(self.v1 != self.v2)
        
if __name__ == '__main__':
    unittest.main()
