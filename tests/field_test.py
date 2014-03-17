# -*- coding: utf-8 -*-
from validator import field, rules
import unittest

class FieldTest(unittest.TestCase):
    def test_single_rule_pass(self):
        f = 'username'
        v = 'wilhelm'
        mn = 3
        mx = 10

        r = field.Field(f, v).append(rules.IsLengthBetween(mn, mx)).run()

        self.assertTrue(r[0])
        self.assertEquals(r[1], [])
        self.assertEquals(len(r), 2)

    def test_single_rule_fail(self):
        f = 'username'
        v = 'wilhelm'
        mn = 3
        mx = 4

        r = field.Field(f, v).append(rules.IsLengthBetween(mn, mx)).run()

        self.assertFalse(r[0])
        self.assertEquals(len(r[1]), 1)
        self.assertEquals(r[1][0], 'String `{}` length is not within `{}` and `{}`'.format(v, mn, mx))
        self.assertEquals(len(r), 2)

    def test_composite_rule_pass(self):
        f = 'username'
        v = 'wilhelm'
        mn = 3
        mx = 10

        r = field.Field(f, v).append([
              rules.IsRequired()
            , rules.IsAlphaNumeric()
            , rules.IsLengthBetween(mn, mx)
        ]).run()

        self.assertTrue(r[0])
        self.assertEquals(r[1], [])
        self.assertEquals(len(r), 2)

    def test_composite_rule_fail(self):
        f = 'username'
        v = 'wilhelm'
        mn = 3
        mx = 4

        r = field.Field(f, v).append([
              rules.IsRequired()
            , rules.IsNumeric()
            , rules.IsLengthBetween(mn, mx)
        ]).run()

        self.assertFalse(r[0])
        self.assertEquals(len(r[1]), 1)
        self.assertEquals(r[1][0], 'This is not a number.')
        self.assertEquals(len(r), 2)

    def test_composite_rule_multiple_fail_messages(self):
        f = 'username'
        v = 'wilhelm'
        mn = 3
        mx = 4

        r = field.Field(f, v, False).append([
              rules.IsRequired()
            , rules.IsNumeric()
            , rules.IsLengthBetween(mn, mx)
        ]).run()

        self.assertFalse(r[0])
        self.assertEquals(len(r[1]), 2)
        self.assertEquals(r[1][0], 'This is not a number.')
        self.assertEquals(r[1][1], 'String `{}` length is not within `{}` and `{}`'.format(v, mn, mx))
        self.assertEquals(len(r), 2)
