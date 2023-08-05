import timeit

number = 1000000
repeat = 3

test_pyeigen = True
test_numpy = True
test_euclid = True
test_vectypes = True
test_cgkit1 = True
test_cgkit2 = True

v1 = None
v2 = None

def test(stmt, setup):
    return timeit.repeat(stmt, setup, repeat=repeat, number=number)

def run_tests():
    global v1, v2

    # Pyeigen
    try:
        import pyeigen
    except ImportError:
        pyeigen = None
    
    if test_pyeigen and pyeigen is not None:
        print "PyEigen"
        v1 = pyeigen.Vector3f(1, 2, 3)
        v2 = pyeigen.Vector3f(4, 5, 6)
        setup = "from __main__ import v1, v2"
    
        print "Add:", test("v1 + v2", setup) 
        print "Multiply:", test("v1 * 2.0", setup)
        print "Dot product:", test("v1.dot(v2)", setup)
        print "Cross product:", test("v1.cross(v2)", setup)
        print
    
    # Numpy
    try:
        import numpy
    except ImportError:
        numpy = None
    
    if test_numpy and numpy is not None:
        print "NumPy"
        v1 = numpy.array([1, 2, 3], dtype=numpy.float32)
        v2 = numpy.array([4, 5, 6], dtype=numpy.float32)
        setup = "from __main__ import v1, v2; from numpy import cross, vdot"
    
        print "Add:", test("v1 + v2", setup)
        print "Multiply:", test("v1 * 2.0", setup)
        print "Dot product:", test("vdot(v1, v2)", setup)
        print "Cross product:", test("cross(v1, v2)", setup)
        print
    
    # euclid
    try:
        import euclid
    except ImportError:
        euclid = None
        
    if test_euclid and euclid is not None:
        print "euclid"
        v1 = euclid.Vector3(1, 2, 3)
        v2 = euclid.Vector3(4, 5, 6)
        setup = "from __main__ import v1, v2"
    
        print "Add:", test("v1 + v2", setup)
        print "Multiply:", test("v1 * 2.0", setup)
        print "Dot product:", test("v1.dot(v2)", setup)
        print "Cross product:", test("v1.cross(v2)", setup)
        print
    
    # vectypes
    try:
        import vectypes
    except ImportError:
        vectypes = None
        
    if test_vectypes and vectypes is not None:
        print "vectypes"
        v1 = vectypes.vec3(1, 2, 3)
        v2 = vectypes.vec3(4, 5, 6)
        setup = "from __main__ import v1, v2; from vectypes import dot, cross"
    
        print "Add:", test("v1 + v2", setup)
        print "Multiply:", test("v1 * 2.0", setup)
        print "Dot product:", test("dot(v1, v2)", setup)
        print "Cross product:", test("cross(v1, v2)", setup)
        print
    
    # cgkit1
    try:
        import cgtypes
    except ImportError:
        cgtypes = None
        
    if test_cgkit1 and cgtypes is not None:
        print "cgkit1"
        v1 = cgtypes.vec3(1, 2, 3)
        v2 = cgtypes.vec3(4, 5, 6)
        setup = "from __main__ import v1, v2"
    
        print "Add:", test("v1 + v2", setup)
        print "Multiply:", test("v1 * 2.0", setup)
        print "Dot product:", test("v1 * v2", setup)
        print "Cross product:", test("v1.cross(v2)", setup)
        print
    
    # cgkit2
    try:
        import cgkit
        import cgkit.cgtypes
    except ImportError:
        cgkit = None
        
    if test_cgkit2 and cgkit is not None:
        print "cgkit2"
        v1 = cgkit.cgtypes.vec3(1, 2, 3)
        v2 = cgkit.cgtypes.vec3(4, 5, 6)
        setup = "from __main__ import v1, v2"
    
        print "Add:", test("v1 + v2", setup)
        print "Multiply:", test("v1 * 2.0", setup)
        print "Dot product:", test("v1 * v2", setup)
        print "Cross product:", test("v1.cross(v2)", setup)
        print

if __name__ == "__main__":
    run_tests()
