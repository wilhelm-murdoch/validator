# -*- coding: utf-8 -*-
from validator import validator, field, rules
import unittest

class ValidatorTest(unittest.TestCase):
    def setUp(self):
        self.v = validator.Validator().append([
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
        ])

    def test_form(self):
        f = self.v.form()
        
        self.assertEquals(f['username'], 'wilhelm')
        self.assertEquals(f['email'], 'wilhelm@gmail.com')
        self.assertEquals(f['password'], 'root')
        self.assertEquals(f['password-confirm'], 'root')

    def test_validator_pass(self):
        self.assertTrue(self.v.run())

    def test_validator_pass_collated_results(self):
        r = self.v.run(True)

        self.assertTrue(type(r), dict)
        self.assertEquals(len(r), 4)

        for f in r:
            self.assertTrue(f['passed'])
            self.assertIsNone(f['errors'])

    def test_validator_fail(self):
        self.v.append(
            field.Field('foo', 'bar').append([
                  rules.IsLengthBetween(1, 1)
                , rules.IsEmail()
            ])
        )

        r = self.v.run()

        self.assertFalse(r)

    def test_validator_fail_collated_results(self):
        self.v.append(
            field.Field('foo', 'bar').append([
                  rules.IsLengthBetween(1, 1)
                , rules.IsEmail()
            ])
        )

        r = self.v.run(True)

        self.assertTrue(type(r), dict)
        self.assertEquals(len(r), 5)

        for f in r:
            if f['field'] == 'foo':
                self.assertFalse(f['passed'])
                self.assertEquals(len(f['errors']), 1)
