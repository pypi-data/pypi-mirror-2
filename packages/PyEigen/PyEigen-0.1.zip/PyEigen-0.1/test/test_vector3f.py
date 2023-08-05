import math
import unittest

from pyeigen import RowVector3f, Vector3f

from settings import TEST_PRECISION

 
class TestVector3fCreate(unittest.TestCase):
    def test_constructor_default(self):
        v = Vector3f()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)

    def test_constructor_arguments(self):
        v = Vector3f(1, 2, 3)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def test_zero(self):
        v = Vector3f.zero()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)

    def test_ones(self):
        v = Vector3f.ones()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 1)
        self.assertEqual(v.z, 1)

    def test_constant(self):
        v = Vector3f.constant(2)
        self.assertEqual(v.x, 2)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 2)

    def test_random(self):
        v = Vector3f.random()
        self.assert_(v.x > -1)
        self.assert_(v.x < 1)
        self.assert_(v.y > -1)
        self.assert_(v.y < 1)
        self.assert_(v.z > -1)
        self.assert_(v.z < 1)

    def test_unit_x(self):
        v = Vector3f.unit_x()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)

    def test_unit_y(self):
        v = Vector3f.unit_y()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 1)
        self.assertEqual(v.z, 0)

    def test_unit_z(self):
        v = Vector3f.unit_z()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 1)

class TestVector3f(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector3f(-1, -2, -3)
        self.v2 = Vector3f(-4, -5, -6)

    def test_set(self):
        self.v1.set(1, 2, 3)
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 3)
    
    def test_set_zero(self):
        self.v1.set_zero()
        self.assertEqual(self.v1.x, 0)
        self.assertEqual(self.v1.y, 0)
        self.assertEqual(self.v1.z, 0)
    
    def test_set_ones(self):
        self.v1.set_ones()
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 1)
        self.assertEqual(self.v1.z, 1)
    
    def test_set_constant(self):
        self.v1.set_constant(2)
        self.assertEqual(self.v1.x, 2)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 2)
    
    def test_set_random(self):
        self.v1.set_random()
        self.assert_(self.v1.x > -1)
        self.assert_(self.v1.x < 1)
        self.assert_(self.v1.y > -1)
        self.assert_(self.v1.y < 1)
        self.assert_(self.v1.z > -1)
        self.assert_(self.v1.z < 1)

    def test_norm(self):
        v = Vector3f(1, 0, 0)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = Vector3f(0, 1, 0)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = Vector3f(0, 0, 1)
        self.assertAlmostEqual(v.norm, 1.0, TEST_PRECISION)
        v = Vector3f(1, 1, 1)
        self.assertAlmostEqual(v.norm, math.sqrt(3), TEST_PRECISION)

    def test_norm_sq(self):
        v = Vector3f(1, 0, 0)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = Vector3f(0, 1, 0)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = Vector3f(0, 0, 1)
        self.assertAlmostEqual(v.norm_sq, 1.0, TEST_PRECISION)
        v = Vector3f(1, 1, 1)
        self.assertAlmostEqual(v.norm_sq, 3, TEST_PRECISION)

    def test_normalized(self):
        self.assertAlmostEqual(self.v1.normalized.norm, 1.0, TEST_PRECISION)
        self.assertAlmostEqual(self.v2.normalized.norm, 1.0, TEST_PRECISION)

    def test_transpose(self):
        rv1 = self.v1.transpose
        self.assertEqual(self.v1.x, rv1.x)
        self.assertEqual(self.v1.y, rv1.y)
        self.assertEqual(self.v1.z, rv1.z)

        self.v1.transpose = RowVector3f(1, 2, 3)
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 3)

    def test_dot(self):
        v1 = Vector3f(0, 0, 0)
        v2 = Vector3f(1, 1, 1)
        self.assertEqual(v1.dot(v1), 0)
        self.assertEqual(v1.dot(v2), 0)
        self.assertEqual(v2.dot(v2), 3)

    def test_cross(self):
        x = Vector3f.unit_x()
        y = Vector3f.unit_y()
        z = Vector3f.unit_z()
        self.assertEqual(x.cross(y), z)
        self.assertEqual(y.cross(z), x)
        self.assertEqual(z.cross(x), y)
        self.assertEqual(y.cross(x), -z)
        self.assertEqual(z.cross(y), -x)
        self.assertEqual(x.cross(z), -y)

    def test_normalize(self):
        self.v1.normalize()
        self.v2.normalize()
        self.assertAlmostEqual(self.v1.norm, 1.0, TEST_PRECISION)
        self.assertAlmostEqual(self.v2.norm, 1.0, TEST_PRECISION)

    def test_add(self):
        v3 = self.v1 + self.v2
        self.assertEqual(v3.x, -5)
        self.assertEqual(v3.y, -7)
        self.assertEqual(v3.z, -9)

    def test_sub(self):
        v3 = self.v1 - self.v2
        self.assertEqual(v3.x, 3)
        self.assertEqual(v3.y, 3)
        self.assertEqual(v3.z, 3)

    def test_mul(self):
        v3 = self.v1 * 2
        self.assertEqual(v3.x, -2)
        self.assertEqual(v3.y, -4)
        self.assertEqual(v3.z, -6)

    def test_div(self):
        v3 = self.v1 / 2
        self.assertEqual(v3.x, -0.5)
        self.assertEqual(v3.y, -1)
        self.assertEqual(v3.z, -1.5)

    def test_negative(self):
        v3 = -self.v1
        self.assertEqual(v3.x, 1)
        self.assertEqual(v3.y, 2)
        self.assertEqual(v3.z, 3)
        v4 = -v3
        self.assertEqual(v4.x, -1)
        self.assertEqual(v4.y, -2)
        self.assertEqual(v4.z, -3)

    def test_inplace_add(self):
        self.v1 += self.v2
        self.assertEqual(self.v1.x, -5)
        self.assertEqual(self.v1.y, -7)
        self.assertEqual(self.v1.z, -9)

    def test_inplace_sub(self):
        self.v1 -= self.v2
        self.assertEqual(self.v1.x, 3)
        self.assertEqual(self.v1.y, 3)
        self.assertEqual(self.v1.z, 3)

    def test_inplace_mul(self):
        self.v1 *= 2
        self.assertEqual(self.v1.x, -2)
        self.assertEqual(self.v1.y, -4)
        self.assertEqual(self.v1.z, -6)

    def test_inplace_div(self):
        self.v1 /= 2
        self.assertEqual(self.v1.x, -0.5)
        self.assertEqual(self.v1.y, -1)
        self.assertEqual(self.v1.z, -1.5)

    def test_len(self):
        self.assertEqual(len(self.v1), 3)

    def test_get_item(self):
        self.assertEqual(self.v1[0], self.v1.x)
        self.assertEqual(self.v1[1], self.v1.y)
        self.assertEqual(self.v1[2], self.v1.z)

    def test_get_slice(self):
        x, y, z = self.v1[:]
        self.assertEqual(x, self.v1.x)
        self.assertEqual(y, self.v1.y)
        self.assertEqual(z, self.v1.z)

    def test_set_item(self):
        self.v1.x = 1
        self.v1.y = 2
        self.v1.z = 3
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 3)
        
    def test_set_slice(self):
        self.v1[:] = 1, 2, 3
        self.assertEqual(self.v1.x, 1)
        self.assertEqual(self.v1.y, 2)
        self.assertEqual(self.v1.z, 3)

    def test_eq(self):
        self.assert_(self.v1 == self.v1)
        self.assertFalse(self.v1 == self.v2)
        
    def test_ne(self):
        self.assertFalse(self.v1 != self.v1)
        self.assert_(self.v1 != self.v2)
        
if __name__ == '__main__':
    unittest.main()
