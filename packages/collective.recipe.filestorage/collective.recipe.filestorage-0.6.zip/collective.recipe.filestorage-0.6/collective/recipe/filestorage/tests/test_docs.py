# -*- coding: utf-8 -*-
"""
Doctest runner for 'collective.recipe.filestorage'.
"""
__docformat__ = 'restructuredtext'

import os
import unittest
import zc.buildout.tests
import zc.buildout.testing

from zope.testing import doctest, renormalizing

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)
                
current_dir = os.path.abspath(os.path.dirname(__file__))
recipe_location = current_dir
zope2_location = os.path.join(current_dir, 'zope2')

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install any other recipes that should be available in the tests
    zc.buildout.testing.install('plone.recipe.zope2instance', test)
    zc.buildout.testing.install('zc.recipe.egg', test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('collective.recipe.filestorage', test)
    
    # Add a base.cfg we can extend
    zc.buildout.testing.write('base.cfg', '''
[buildout]
index = http://pypi.python.org/simple
versions = versions
[versions]
# pin to a version that doesn't pull in an eggified Zope
plone.recipe.zope2instance = 3.6
''')


def test_suite():
    suite = unittest.TestSuite((
            doctest.DocFileSuite(
                '../README.txt',
                setUp=setUp,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        ]),
                globs = globals()
                ),
            ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
