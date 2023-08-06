__author__ = "Jon Reid"
__copyright__ = "Copyright 2010 www.hamcrest.org"
__license__ = "BSD, see License.txt"
__version__ = "1.0"

from hamcrest.core.base_matcher import BaseMatcher


class IsIn(BaseMatcher):
    """Is the value present in the given sequence?"""

    def __init__(self, sequence):
        self.sequence = sequence

    def _matches(self, item):
        return item in self.sequence

    def describe_to(self, description):
        description.append_text('one of ')      \
                    .append_value_list('(', ', ', ')', self.sequence)


def is_in(sequence):
    """Is the value present in the given sequence?"""
    return IsIn(sequence)
