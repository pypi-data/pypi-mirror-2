import timeit

number = 1000000
repeat = 3

test_pyeigen = True
test_numpy = True
test_euclid = True
test_vectypes = True
test_cgkit1 = True
test_cgkit2 = True

m1 = None
m2 = None

def test(stmt, setup):
    return timeit.repeat(stmt, setup, repeat=repeat, number=number)

def run_tests():
    global m1, m2

    # Pyeigen
    try:
        import pyeigen
    except ImportError:
        pyeigen = None
    
    if test_pyeigen and pyeigen is not None:
        print "PyEigen"
        m1 = pyeigen.Matrix4f()
        m2 = pyeigen.Matrix4f()
        m1.set_zero()
        m2.set_ones()
        setup = "from __main__ import m1, m2"
    
        print "Add:", test("m1 + m2", setup) 
        print "Multiply:", test("m1 * m2", setup)
        print "Scalar multiply:", test("m1 * 2.0", setup)
        print
    
    # Numpy
    try:
        import numpy
    except ImportError:
        numpy = None
    
    if test_numpy and numpy is not None:
        print "NumPy"
        m1 = numpy.zeros((4, 4), dtype=numpy.float32)
        m2 = numpy.ones((4, 4), dtype=numpy.float32)
        setup = "from __main__ import m1, m2"
    
        print "Add:", test("m1 + m2", setup)
        print "Multiply:", test("m1 * m2", setup)
        print "Scalar multiply:", test("m1 * 2.0", setup)
        print
    
    # euclid
    try:
        import euclid
    except ImportError:
        euclid = None
        
    if test_euclid and euclid is not None:
        print "euclid"
        m1 = euclid.Matrix4()
        m2 = euclid.Matrix4()
        setup = "from __main__ import m1, m2"
    
        # Euclid doesn't support matrix addition and scalar multiply
    #    print "Add:", test("m1 + m2", setup)
        print "Multiply:", test("m1 * m2", setup)
    #    print "Scalar multiply:", test("m1 * 2.0", setup)
        print
    
    # vectypes
    try:
        import vectypes
    except ImportError:
        vectypes = None
        
    if test_vectypes and vectypes is not None:
        print "vectypes"
        m1 = vectypes.mat4()
        m2 = vectypes.mat4()
        setup = "from __main__ import m1, m2"
    
        print "Add:", test("m1 + m2", setup)
        print "Multiply:", test("m1 * m2", setup)
        print "Scalar multiply:", test("m1 * 2.0", setup)
        print
    
    # cgkit1
    try:
        import cgtypes
    except ImportError:
        cgtypes = None
        
    if test_cgkit1 and cgtypes is not None:
        print "cgkit1"
        m1 = cgtypes.mat4()
        m2 = cgtypes.mat4()
        setup = "from __main__ import m1, m2"
    
        print "Add:", test("m1 + m2", setup)
        print "Multiply:", test("m1 * m2", setup)
        print "Scalar multiply:", test("m1 * 2.0", setup)
        print
    
    # cgkit2
    try:
        import cgkit
        import cgkit.cgtypes
    except ImportError:
        cgkit = None
        
    if test_cgkit2 and cgkit is not None:
        print "cgkit2"
        m1 = cgkit.cgtypes.mat4()
        m2 = cgkit.cgtypes.mat4()
        setup = "from __main__ import m1, m2"
    
        print "Add:", test("m1 + m2", setup)
        print "Multiply:", test("m1 * m2", setup)
        print "Scalar multiply:", test("m1 * 2.0", setup)
        print

if __name__ == "__main__":
    run_tests()
