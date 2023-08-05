import unittest
import doctest

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        doctest.DocTestSuite('collective.dnifield.field',
                             optionflags=doctest.ELLIPSIS),
        ])
    return suite
