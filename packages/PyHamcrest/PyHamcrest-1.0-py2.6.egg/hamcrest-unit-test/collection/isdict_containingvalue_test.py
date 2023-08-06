__author__ = "Jon Reid"
__copyright__ = "Copyright 2010 www.hamcrest.org"
__license__ = "BSD, see License.txt"
__version__ = "1.0"

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '..')
    sys.path.insert(0, '../..')

import unittest

from hamcrest.core.core.isequal import equal_to
from hamcrest.library.collection.isdict_containingvalue import has_value

from matcher_test import MatcherTest
from quasidict import QuasiDictionary


class IsDictContainingValueTest(MatcherTest):

    def testHasReadableDescription(self):
        self.assert_description("dictionary with value 'a'", has_value('a'))

    def testDoesNotMatchEmptyMap(self):
        self.assert_does_not_match('Empty dictionary', has_value(1), {});

    def testMatchesSingletonDictContainingValue(self):
        d = {'a': 1}
        self.assert_matches('Matches single value', has_value(equal_to(1)), d)

    def testMatchesDictContainingValue(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assert_matches('has_value 1', has_value(equal_to(1)), d)
        self.assert_matches('has_value 3', has_value(equal_to(3)), d)

    def testProvidesConvenientShortcutForMatchingWithIsEqualTo(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assert_matches('Matches c', has_value(3), d)

    def testDoesNotMatchMapMissingValue(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assert_does_not_match('Dictionary without matching value',
                                    has_value(4), d)

    def testMatchesQuasiDictionary(self):
        self.assert_matches('quasi', has_value('1'), QuasiDictionary())
        self.assert_does_not_match('other', has_value('1'), object())


if __name__ == '__main__':
    unittest.main()
