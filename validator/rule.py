# -*- coding: utf-8 -*-

class Rule(object):
    """ Base abstract class representing a rule. All defined rules must be derived from this class. """
    def __init__(self, error = None, pass_on_blank = False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        self.error = error
        self.pass_on_blank = pass_on_blank


    def run(self, field_value):
        """ Invoked once a defined rule is ready to be validated. """
        raise NotImplementedError('This method cannot be accessed directly')