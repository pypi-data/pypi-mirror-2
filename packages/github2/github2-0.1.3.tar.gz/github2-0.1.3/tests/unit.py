# -*- coding: latin-1 -*-
import unittest

from github2.issues import Issue


class ReprTests(unittest.TestCase):
    """__repr__ must return strings, not unicode objects."""

    def test_issue(self):
        """Issues can have non-ASCII characters in the title."""
        i = Issue(title = u'abcdé')
        self.assertEqual(str, type(repr(i)))
