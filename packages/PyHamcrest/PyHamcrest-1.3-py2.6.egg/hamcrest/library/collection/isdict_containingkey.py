__author__ = "Jon Reid"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.hasmethod import hasmethod
from hamcrest.core.helpers.wrap_matcher import wrap_matcher


class IsDictContainingKey(BaseMatcher):
    """Matches dictionaries containing a key satisfying a given matcher."""

    def __init__(self, key_matcher):
        self.key_matcher = key_matcher

    def _matches(self, dictionary):
        if hasmethod(dictionary, 'keys'):
            for key in dictionary.keys():
                if self.key_matcher.matches(key):
                    return True
        return False

    def describe_to(self, description):
        description.append_text('a dictionary containing key ')     \
                    .append_description_of(self.key_matcher)

#------------------------------------------------------------------------------

def has_key(key):
    """Matches dictionaries containing a key satisfying a given matcher.

    :param key: A matcher - or a value for
        :py:func:`~hamcrest.core.core.isequal.equal_to` matching - for the key.

    """
    return IsDictContainingKey(wrap_matcher(key))
