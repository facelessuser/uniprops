"""Test `Word Break`."""
import unittest
import uniprops
import re


class TestWordBreak(unittest.TestCase):
    """Test `Word Break` access."""

    def test_table_integrity(self):
        """Test that there is parity between Unicode and ASCII tables."""

        re_key = re.compile(r'^\^?[a-z0-9./]+$')

        keys1 = set(uniprops.unidata.unicode_word_break.keys())
        keys2 = set(uniprops.unidata.ascii_word_break.keys())

        # Ensure all keys are lowercase (only need to check Unicode as the ASCII keys must match the Unicode later)
        for k in keys1:
            self.assertTrue(re_key.match(k) is not None)

        # Ensure the same keys are in both the Unicode table as the ASCII table
        self.assertEqual(keys1, keys2)

        # Ensure each positive key has an inverse key
        for key in keys1:
            if not key.startswith('^'):
                self.assertTrue('^' + key in keys1)

    def test_wordbreak(self):
        """Test `Word Break` properties."""

        for k, v in uniprops.unidata.unicode_word_break.items():
            result = uniprops.get_unicode_property('wordbreak', k)
            self.assertEqual(result, v)

    def test_wordbreak_ascii(self):
        """Test `Word Break` ASCII properties."""

        for k, v in uniprops.unidata.ascii_word_break.items():
            result = uniprops.get_unicode_property('wordbreak', k, limit_ascii=True)
            self.assertEqual(result, v)

    def test_bad_wordbreak(self):
        """Test `Word Break` property with bad value."""

        with self.assertRaises(ValueError):
            uniprops.get_unicode_property('wordbreak', 'bad')

    def test_alias(self):
        """Test aliases."""

        alias = None
        for k, v in uniprops.unidata.alias.unicode_alias['_'].items():
            if v == 'wordbreak':
                alias = k
                break

        self.assertTrue(alias is not None)

        # Ensure alias works
        for k, v in uniprops.unidata.unicode_word_break.items():
            result = uniprops.get_unicode_property(alias, k)
            self.assertEqual(result, v)
            break

        # Test aliases for values
        for k, v in uniprops.unidata.alias.unicode_alias['wordbreak'].items():
            result1 = uniprops.get_unicode_property(alias, k)
            result2 = uniprops.get_unicode_property(alias, v)
            self.assertEqual(result1, result2)
