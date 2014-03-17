# -*- coding: utf-8 -*-
from validator import validator, field, rules
import unittest

class ValidatorTest(unittest.TestCase):
    def test_validator(self):
        v = validator.Validator().append([
            field.Field('username', 'wilhelm').append([
                  rules.IsRequired()
                , rules.IsAlphaNumeric()
                , rules.IsLengthBetween(3, 10)
            ]),
            field.Field('email', 'wilhelm@gmail.com').append([
                  rules.IsRequired()
                , rules.IsEmail()
            ]),
            field.Field('password', 'root').append([
                  rules.IsRequired()
                , rules.IsLengthBetween(2, 10)
            ]),
            field.Field('password-confirm', 'root').append([
                rules.Matches('root')
            ]),
        ]).run()

        self.assertTrue(v)