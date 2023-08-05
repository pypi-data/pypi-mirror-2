import unittest
import doctest

from Testing import ZopeTestCase as ztc

from getpaid.SalesforcePloneFormGenAdapter.tests import base

testfiles = (
    'pfg_adapter_view.txt',
)

def test_suite():
    return unittest.TestSuite([

        # Test the control panel
        ztc.FunctionalDocFileSuite(
            f, package='getpaid.SalesforcePloneFormGenAdapter.tests',
            test_class=base.BaseGetPaidPFGSalesforceAdapterFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
        
            for f in testfiles
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
