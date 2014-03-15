# -*- coding: utf-8 -*-
from validator import rules
import unittest

class RulesTest(unittest.TestCase):
    def test_matches(self):
        s1 = 'merp'
        s2 = 'merp'
        s3 = 'prem'

        r = rules.Matches(s1).run(s2)
        self.assertTrue(r)

        r = rules.Matches(s1).run(s3)
        self.assertFalse(r)

    def test_regex(self):
        n1 = '1'
        n2 = '10'
        n3 = 'foo'
        regex = '^[0-1]+$'
        
        r = rules.Regex(regex).run(n1)
        self.assertTrue(r)

        r = rules.Regex(regex).run(n2)
        self.assertTrue(r)

        r = rules.Regex(regex).run(n3)
        self.assertFalse(r)

    def test_is_email(self):
        e1 = 'wilhelm.murdoch@gmail.com'
        e2 = ',1320df9d,3.9kd'
        
        r = rules.IsEmail().run(e1)
        self.assertTrue(r)

        r = rules.IsEmail().run(e2)
        self.assertFalse(r)        

    def test_is_numeric(self):
        s1 = '1'
        s2 = 'b'

        r = rules.IsNumeric().run(s1)
        self.assertTrue(r)

        r = rules.IsNumeric().run(s2)
        self.assertFalse(r)       

    def test_is_alpha(self):
        s1 = 'abc'
        s2 = '123'

        r = rules.IsAlpha().run(s1)
        self.assertTrue(r)

        r = rules.IsAlpha().run(s2)
        self.assertFalse(r)  

    def test_is_alpha_numeric(self):
        s1 = 'abc123'
        s2 = ')(*&^&%^#$'

        r = rules.IsAlphaNumeric().run(s1)
        self.assertTrue(r)

        r = rules.IsAlphaNumeric().run(s2)
        self.assertFalse(r)  

    def test_is_required(self):
        s1 = 'abc'
        s2 = ''

        r = rules.IsRequired().run(s1)
        self.assertTrue(r)

        r = rules.IsRequired().run(s2)
        self.assertFalse(r)  

    def test_is_length(self):
        s1 = 'abc'
        l1 = 3
        l2 = 2

        r = rules.IsLength(l1).run(s1)
        self.assertTrue(r)

        r = rules.IsLength(l2).run(s1)
        self.assertFalse(r)  

    def test_is_length_between(self):
        s1 = 'abc'
        mn1 = 1
        mn2 = 6
        mx1 = 8
        mx2 = 3

        r = rules.IsLengthBetween(mn1, mx1).run(s1)
        self.assertTrue(r)

        r = rules.IsLengthBetween(mn2, mx2).run(s1)
        self.assertFalse(r) 

    def test_is_in_list(self):
        l = [1, 2, 3, 4, 5]
        i1 = 4
        i2 = 10

        r = rules.IsInList(l).run(i1)
        self.assertTrue(r)

        r = rules.IsInList(l).run(i2)
        self.assertFalse(r) 

    def test_is_type(self):
        t1 = ()
        t2 = {}
        t3 = []

        r = rules.IsType(t1).run(tuple())
        self.assertTrue(r)

        r = rules.IsType(t2).run(dict())
        self.assertTrue(r)

        r = rules.IsType(t3).run(list())
        self.assertTrue(r)

        r = rules.IsType(t3).run(tuple())
        self.assertFalse(r)

        r = rules.IsType(t1).run(dict())
        self.assertFalse(r)

        r = rules.IsType(t2).run(list())
        self.assertFalse(r)