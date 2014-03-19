# -*- coding: utf-8 -*-
from validator import collection, field, rules
import unittest

class CollectionTest(unittest.TestCase):
    def setUp(self):
        self.c = collection.Collection().append([
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
        f = self.c.form()
        
        self.assertEquals(f['username'], 'wilhelm')
        self.assertEquals(f['email'], 'wilhelm@gmail.com')
        self.assertEquals(f['password'], 'root')
        self.assertEquals(f['password-confirm'], 'root')

    def test_validator_pass(self):
        self.assertTrue(self.c.run())
        self.assertIsNone(self.c.errors())

    def test_validator_pass_collated_results(self):
        r = self.c.run(True)

        self.assertTrue(type(r), dict)
        self.assertEquals(len(r), 4)
        self.assertIsNone(self.c.errors())

        for f in r:
            self.assertTrue(f['passed'])
            self.assertIsNone(f['errors'])

    def test_validator_fail(self):
        self.c.append(
            field.Field('foo', 'bar').append([
                  rules.IsLengthBetween(1, 1)
                , rules.IsEmail()
            ])
        )

        r = self.c.run()

        self.assertFalse(r)

    def test_validator_errors(self):
        self.c.append(
            field.Field('foo', 'bar').append(rules.IsLengthBetween(1, 1))
        )

        r = self.c.run(True)
        e = self.c.errors()

        self.assertEquals(type(e), dict)
        self.assertIsNotNone(e['foo'])
        self.assertTrue(len(e['foo']), 1)
        self.assertEquals(e['foo'][0], 'String `bar` length is not within `1` and `1`')

    def test_validator_fail_collated_results(self):
        self.c.append(
            field.Field('foo', 'bar').append([
                  rules.IsLengthBetween(1, 1)
                , rules.IsEmail()
            ])
        )

        r = self.c.run(True)

        self.assertTrue(type(r), dict)
        self.assertEquals(len(r), 5)

        for f in r:
            if f['field'] == 'foo':
                self.assertFalse(f['passed'])
                self.assertEquals(len(f['errors']), 1)
