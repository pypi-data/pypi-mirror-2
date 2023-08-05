import unittest
from doctest import DocTestSuite

from zope.interface import implements
from zope.component import provideUtility
from zif.headincludes.interfaces import IHeadIncludeRegistration
from zif.headincludes import resourcelibrary

class StubHeadIncluder:
    
    implements(IHeadIncludeRegistration)
    
    def register(self, url):
        print url


def test_need_dependencies():
    """
        >>> includedr = StubHeadIncluder()
        >>> provideUtility(includedr, IHeadIncludeRegistration)

        >>> parent = resourcelibrary.LibraryInfo()
        >>> parent.included.append('parent_file')
        >>> resourcelibrary.library_info['parent'] = parent

        >>> intermediate = resourcelibrary.LibraryInfo()
        >>> intermediate.included.append('intermediate_file')
        >>> intermediate.required.append('parent')
        >>> resourcelibrary.library_info['intermediate'] = intermediate

        >>> child = resourcelibrary.LibraryInfo()
        >>> child.included.append('child_file')
        >>> child.required.append('intermediate')
        >>> resourcelibrary.library_info['child'] = child

        >>> resourcelibrary.need('child')
        /@@/parent/parent_file
        /@@/intermediate/intermediate_file
        /@@/child/child_file
    """

def test_suite():
    return DocTestSuite('zif.headincludes.tests')

