import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing, eventtesting

from Testing import ZopeTestCase as ztc

from collective.subscribemember.tests import base

def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            functest, package='collective.subscribemember',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_UDIFF)
            for functest in [
                             'subscribemember.txt',
                             'memberimport.txt',
                             'memberexpiry.txt',
                             'memberexport.txt'
                           ]

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')