# -*- coding: utf-8 -*-
"""
Doctest runner for 'valentine.linguaflow'
"""
__docformat__ = 'restructuredtext'

import base

from zope.testing import doctest
optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(root):
    portal = root.portal
    root.setRoles(['Manager'])
    ourId = portal.invokeFactory('Folder', id='folder')
    portal.portal_workflow.doActionFor(portal[ourId], 'publish')

def test_suite():
    from unittest import TestSuite
    suite = TestSuite()
    from Testing.ZopeTestCase import ZopeDocFileSuite
    suite.addTest(ZopeDocFileSuite(
                'README.txt',
                setUp=setUp,
                #tearDown=tearDown,
                package="valentine.linguaflow",
                test_class=base.ValentineLinguaflowFunctionalTestCase,
                optionflags=optionflags),
                )
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
