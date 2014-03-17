# -*- coding: utf-8 -*-

class Rule(object):
    """ Base abstract class representing a "rule". All defined rules must be derived from this class. """

    error = None
    """ User-defined error message for a failed rule. """

    pass_on_blank = False
    """ Pass through as success if field value is blank. Useful if you only want to validate fields with actual values. """

    def __init__(self, error = None, pass_on_blank = False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """

        super(Rule, self).__init__()
        self.error = error
        self.pass_on_blank = pass_on_blank


    def run(self, field_value):
        """ Invoked once a defined rule is ready to be validated. """

        raise NotImplementedError('This method cannot be accessed directly')