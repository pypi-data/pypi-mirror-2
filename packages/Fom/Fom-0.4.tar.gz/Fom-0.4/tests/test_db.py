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

if __name__ == '__main__':
    unittest.main()
