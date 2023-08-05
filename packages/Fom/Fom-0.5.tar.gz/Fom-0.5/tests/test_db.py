import unittest

from fom.db import FluidDB
from fom.errors import Fluid404Error


class TestDB(unittest.TestCase):

    def test_default(self):
        db = FluidDB('http://sandbox.fluidinfo.com')
        self.assertEquals(db.base_url, 'http://sandbox.fluidinfo.com')

    def test_call(self):
        db = FluidDB('http://sandbox.fluidinfo.com')
        r = db('GET', '/users/aliafshar')
        self.assertEquals(r.value['name'], u'aliafshar')

    def test_call_nasty(self):
        """
        Ensures that a path is properly "quoted" so, for example, a space
        maps to %20
        """
        db = FluidDB('http://sandbox.fluidinfo.com')
        self.assertRaises(Fluid404Error, db, 'GET', '/users/a name')

    def test_trailing_slash_handling(self):
        """
        Make sure we get a complaint if the base URL for the instance
        of fluiddb ends with a slash.

        BAD: http://fluiddb.fluidinfo.com/
        GOOD: http://fluiddb.fluidinfo.com

        Why not knock off the trailing slash..? Well, it's easy to complain
        but hard to second guess the caller's intention
        """
        # Bad
        self.assertRaises(ValueError, FluidDB,
                          'http://sandbox.fluidinfo.com/')
        # Good
        self.assertTrue(FluidDB('http://sandbox.fluidinfo.com'))

if __name__ == '__main__':
    unittest.main()
