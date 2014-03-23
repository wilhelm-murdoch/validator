# -*- coding: utf-8 -*-
import rule

class Field(object):
    """ Represents the concept of a field."""
    def __init__(self, title, value, stop_on_first_error=True):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        title str                -- The title of this field.
        value str                -- The value associated with this field.
        stop_on_first_error bool -- Will break out of applying rules when it first encounters an error.
        """
        self.rules = []
        self.title = title
        self.value = value
        self.stop_on_first_error = stop_on_first_error

    def __iter__(self):
        """ Returns generator to iterate through assigned rules. """
        for rule in self.rules:
            yield rule

    def __len__(self):
        """ Implements built-in len() to return number of assigned rules. """
        return len(self.rules)

    def __getitem__(self, i):
        """ Allows for self[key] access. Will raise IndexError if out of range. """
        return self.rules[i]

    def append(self, _rule):
        """ Attaches an instance of class Rule to the current instance of this Field

        Keyword arguments:
        rule object -- Instance of class Rule to apply to this field.
        """
        if isinstance(_rule, list):
            for r in _rule:
                if not isinstance(r, rule.Rule):
                    raise TypeError('parameter :rule must be list of class Rule instances')
                self.rules.append(r)
            return self
        elif not isinstance(_rule, rule.Rule):
            raise TypeError('parameter :rule must be instance of class Rule')
        self.rules.append(_rule)
        return self

    def run(self):
        """ Iterates through all associated rules, executes them and collects the results. """
        errors = []
        for rule in self.rules:
            if not rule.run(self.value):
                errors.append(rule.error)
                if self.stop_on_first_error:
                    break
        return False if errors else True, errors