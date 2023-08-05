import math
import unittest

from pyeigen import RowVector4f, Vector4f

from settings import TEST_PRECISION

 
class TestVector4fCreate(unittest.TestCase):
    def test_constructor_default(self):
        v = Vector4f()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)
        self.assertEqual(v.w, 0)

    def test_constructor_arguments(self):
        v = Vector4f(1, 2, 3, 4)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)
        self.assertEqual(v.w, 4)

    def test_zero(self):
        v = Vector4f.zero()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)
        self.assertEqual(v.w, 0)

    def test_ones(self):
        v = Vector4f.ones()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 1)
        self.assertEqual(v.z, 1)
        self.assertEqual(v.w, 1)

    def test_constant(self):
        v = Vector4f.constant(2)
        self.assertEqual(v.x, 2)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 2)
        self.assertEqual(v.w, 2)

    def test_random(self):
        v = Vector4f.random()
        self.assert_(v.x > -1)
        self.assert_(v.x < 1)
        self.assert_(v.y > -1)
        self.assert_(v.y < 1)
        self.assert_(v.z > -1)
        self.assert_(v.z < 1)
        self.assert_(v.w > -1)
        self.assert_(v.w < 1)

    def test_unit_x(self):
        v = Vector4f.unit_x()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)
        self.assertEqual(v.w, 0)

    def test_unit_y(self):
        v = Vector4f.unit_y()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 1)
        self.assertEqual(v.z, 0)
        self.assertEqual(v.w, 0)

    def test_unit_z(self):
        v = Vector4f.unit_z()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 1)
        self.assertEqual(v.w, 0)

    def test_unit_w(self):
        v = Vector4f.unit_w()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)
        self.assertEqual(v.w, 1)

class TestVector4f(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector4f(-1, -2, -3, -4)
        self.v2 = Vector4f(-5, -6, -7, -8)

    def test_set(self):
        self.v1.set(1, 2, 3, 4)
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 3)
        self.assertEqual(self.v1.w, 4)
    
    def test_set_zero(self):
        self.v1.set_zero()
        self.assertEqual(self.v1.x, 0)
        self.assertEqual(self.v1.y, 0)
        self.assertEqual(self.v1.z, 0)
        self.assertEqual(self.v1.w, 0)
    
    def test_set_ones(self):
        self.v1.set_ones()
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 1)
        self.assertEqual(self.v1.z, 1)
        self.assertEqual(self.v1.w, 1)
    
    def test_set_constant(self):
        self.v1.set_constant(2)
        self.assertEqual(self.v1.x, 2)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 2)
        self.assertEqual(self.v1.w, 2)
    
    def test_set_random(self):
        self.v1.set_random()
        self.assert_(self.v1.x > -1)
        self.assert_(self.v1.x < 1)
        self.assert_(self.v1.y > -1)
        self.assert_(self.v1.y < 1)
        self.assert_(self.v1.z > -1)
        self.assert_(self.v1.z < 1)
        self.assert_(self.v1.w > -1)
        self.assert_(self.v1.w < 1)

    def test_norm(self):
        v = Vector4f(1, 0, 0, 0)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = Vector4f(0, 1, 0, 0)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = Vector4f(0, 0, 1, 0)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = Vector4f(0, 0, 0, 1)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = Vector4f(1, 1, 1, 1)
        self.assertAlmostEqual(v.norm, math.sqrt(4), TEST_PRECISION)

    def test_norm_sq(self):
        v = Vector4f(1, 0, 0, 0)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = Vector4f(0, 1, 0, 0)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = Vector4f(0, 0, 1, 0)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = Vector4f(0, 0, 0, 1)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = Vector4f(1, 1, 1, 1)
        self.assertAlmostEqual(v.norm_sq, 4, TEST_PRECISION)

    def test_dot(self):
        v1 = Vector4f(0, 0, 0, 0)
        v2 = Vector4f(1, 1, 1, 1)
        self.assertEqual(v1.dot(v1), 0)
        self.assertEqual(v1.dot(v2), 0)
        self.assertEqual(v2.dot(v2), 4)

    def test_normalized(self):
        self.assertAlmostEqual(self.v1.normalized.norm, 1.0, TEST_PRECISION)
        self.assertAlmostEqual(self.v2.normalized.norm, 1.0, TEST_PRECISION)

    def test_transpose(self):
        rv1 = self.v1.transpose
        self.assertEqual(self.v1.x, rv1.x)
        self.assertEqual(self.v1.y, rv1.y)
        self.assertEqual(self.v1.z, rv1.z)
        self.assertEqual(self.v1.w, rv1.w)

        self.v1.transpose = RowVector4f(1, 2, 3, 4)
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 3)
        self.assertEqual(self.v1.w, 4)

    def test_normalize(self):
        self.v1.normalize()
        self.v2.normalize()
        self.assertAlmostEqual(self.v1.norm, 1.0, TEST_PRECISION)
        self.assertAlmostEqual(self.v2.norm, 1.0, TEST_PRECISION)

    def test_add(self):
        v3 = self.v1 + self.v2
        self.assertEqual(v3.x, -6)
        self.assertEqual(v3.y, -8)
        self.assertEqual(v3.z, -10)
        self.assertEqual(v3.w, -12)

    def test_sub(self):
        v3 = self.v1 - self.v2
        self.assertEqual(v3.x, 4)
        self.assertEqual(v3.y, 4)
        self.assertEqual(v3.z, 4)
        self.assertEqual(v3.w, 4)

    def test_mul(self):
        v3 = self.v1 * 2
        self.assertEqual(v3.x, -2)
        self.assertEqual(v3.y, -4)
        self.assertEqual(v3.z, -6)
        self.assertEqual(v3.w, -8)

    def test_div(self):
        v3 = self.v1 / 2
        self.assertEqual(v3.x, -0.5)
        self.assertEqual(v3.y, -1)
        self.assertEqual(v3.z, -1.5)
        self.assertEqual(v3.w, -2)

    def test_negative(self):
        v3 = -self.v1
        self.assertEqual(v3.x, 1)
        self.assertEqual(v3.y, 2)
        self.assertEqual(v3.z, 3)
        self.assertEqual(v3.w, 4)
        v4 = -v3
        self.assertEqual(v4.x, -1)
        self.assertEqual(v4.y, -2)
        self.assertEqual(v4.z, -3)
        self.assertEqual(v4.w, -4)

    def test_inplace_add(self):
        self.v1 += self.v2
        self.assertEqual(self.v1.x, -6)
        self.assertEqual(self.v1.y, -8)
        self.assertEqual(self.v1.z, -10)
        self.assertEqual(self.v1.w, -12)

    def test_inplace_sub(self):
        self.v1 -= self.v2
        self.assertEqual(self.v1.x, 4)
        self.assertEqual(self.v1.y, 4)
        self.assertEqual(self.v1.z, 4)
        self.assertEqual(self.v1.w, 4)

    def test_inplace_mul(self):
        self.v1 *= 2
        self.assertEqual(self.v1.x, -2)
        self.assertEqual(self.v1.y, -4)
        self.assertEqual(self.v1.z, -6)
        self.assertEqual(self.v1.w, -8)

    def test_inplace_div(self):
        self.v1 /= 2
        self.assertEqual(self.v1.x, -0.5)
        self.assertEqual(self.v1.y, -1)
        self.assertEqual(self.v1.z, -1.5)
        self.assertEqual(self.v1.w, -2)

    def test_len(self):
        self.assertEqual(len(self.v1), 4)

    def test_get_item(self):
        self.assertEqual(self.v1[0], self.v1.x)
        self.assertEqual(self.v1[1], self.v1.y)
        self.assertEqual(self.v1[2], self.v1.z)
        self.assertEqual(self.v1[3], self.v1.w)

    def test_get_slice(self):
        x, y, z, w = self.v1[:]
        self.assertEqual(x, self.v1.x)
        self.assertEqual(y, self.v1.y)
        self.assertEqual(z, self.v1.z)
        self.assertEqual(w, self.v1.w)

    def test_set_item(self):
        self.v1.x = 1
        self.v1.y = 2
        self.v1.z = 3
        self.v1.w = 4
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 3)
        self.assertEqual(self.v1.w, 4)
        
    def test_set_slice(self):
        self.v1[:] = 1, 2, 3, 4
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 3)
        self.assertEqual(self.v1.w, 4)

    def test_eq(self):
        self.assert_(self.v1 == self.v1)
        self.assertFalse(self.v1 == self.v2)
        
    def test_ne(self):
        self.assertFalse(self.v1 != self.v1)
        self.assert_(self.v1 != self.v2)
        
if __name__ == '__main__':
    unittest.main()
