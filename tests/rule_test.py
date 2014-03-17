# -*- coding: utf-8 -*-
from validator import rule, rules
import unittest

class RuleTest(unittest.TestCase):
    def test_raises_notimplemented_error(self):
        self.assertRaises(NotImplementedError, rule.Rule().run, None)