from inrex import *
import unittest


class TestMain(unittest.TestCase):
    def get_assert_methods(self):
        d = {}
        for attrname in dir(self):
            if attrname.startswith("assert"):
                assert_method = getattr(self, attrname)
                d[attrname] = assert_method
        return d

    def test_chum(self):
        from sys import stdin
        print "\n    RUNNING TESTS\n"
        if "asdasd" |match| r".*(sd).*":
            print "match[1]",  match[1]
        if "aXAbXAc" |split| r"XA":
            print split.result
            #for item in findall:
            #    print item
            print "len",  len(split)
            print "findall[2]",  split[2]
        print '-----------------------'
        import StringIO
        s = StringIO.StringIO()
        s.write('a1b2c3\nx4y5z6\n')
        s.seek(0)
        for i in s |findall| r'\d': print i

    def test_match(self):
        globals().update( self.get_assert_methods())

        #
        # strings as input
        #
        m = "asd 123" |match| r"(\d+) (\w+)"
        assertFalse( bool(m))

        m = "asd 123" |match| r"(\w+) (\d+)"
        assertTrue( bool(m))
        assertTrue( "asd" == m.group(1) )
        assertTrue( "123" == m.group(2) )
        assertTrue( "asd" == match[1] )
        assertTrue( "123" == match[2] )

        m = "asd 123" |match| r"(?P<word>\w+) (?P<digit>\d+)"
        assertTrue( "asd" == match["word"] )
        assertTrue( "123" == match["digit"] )

        #
        # fileish objects as input
        #
        import StringIO

        f = StringIO.StringIO()
        f.write("asd 123\nqwe 456\n")
        f.seek(0)

        i = 0

        for m in (f |match| r"(\w+) (\d+)"):
            if i == 0:
                assertTrue( m.group(1) == "asd")
                assertTrue( m.group(2) == "123")
            if i == 1:
                assertTrue( m.group(1) == "qwe")
                assertTrue( m.group(2) == "456")
            i = i + 1

        assertTrue(
            i == 2
        )



if __name__ == "__main__":
    unittest.main()