# -*- coding: utf-8 -*-
from validator import core, rules
import unittest

class ValidatorTest(unittest.TestCase):
    def test_validator(self):
        v = core.Validator().append([
            core.Field('username', 'wilhelm').append([
                  rules.IsRequired()
                , rules.IsAlphaNumeric()
                , rules.IsLengthBetween(3, 10)
            ]),
            core.Field('email', 'wilhelm@gmail.com').append([
                  rules.IsRequired()
                , rules.IsEmail()
            ]),
            core.Field('password', 'root').append([
                  rules.IsRequired()
                , rules.IsLengthBetween(2, 10)
            ]),
            core.Field('password-confirm', 'root').append([
                rules.Matches('root')
            ]),
        ]).run()

        self.assertTrue(v)