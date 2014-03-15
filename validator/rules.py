# -*- coding: utf-8 -*-
from validator.core import Rule
import re

class Matches(Rule):
    """ Simple rule used to determine whether one value matches another. Commonly used
    for password confirmation. """

    match = ''
    """ The value to compare against the associated field's value. """

    def __init__(self, match, error = None, pass_on_blank = False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        match str          -- The value to compare against the associated field's value.
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        super(Matches, self).__init__(error, pass_on_blank)
        self.match = match


    def run(self, field_value):
        """ Invoked once a defined rule is ready to be validated.

        Keyword arguments:
        field_value str -- the value of the associated field to compare.
        """

        if self.pass_on_blank and not field_value.strip():
            return True

        if self.match != field_value:
            if not self.error:
                self.error = "Values `%s` and `%s` do not match." % (field_value, self.match)
            return False
        return True



class Regex(Rule):
    """ Applies a regular expression to a given field value. """

    expression = ''
    """ The regular expression to apply. """

    def __init__(self, expression, error = None, pass_on_blank = False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        expression str     -- The regular expression to apply to the given field.
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        super(Regex, self).__init__(error, pass_on_blank)
        self.expression = expression


    def run(self, field_value):
        """ Invoked once a defined rule is ready to be validated.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if self.pass_on_blank and not field_value.strip():
            return True

        if not self.expression:
            raise ValueError('This rule requires a regular expression.')

        try:
            regex = re.compile(self.expression)

            if not regex.match(field_value):
                if not self.error:
                    self.error = "Expression `%s` failed when applied to `%s`" % (self.expression, field_value)
                return False
        except Exception, e:
            raise ValueError("Expression `%s` failed with the following error: %s" % (self.expression, e))
        return True



class IsEmail(Regex):
    """ Regex convenience derivative class used to determine if given field value is a
    valid email address. """

    def __init__(self, error = None, pass_on_blank = False):
        super(IsEmail, self).__init__(r'^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', error, pass_on_blank)
        if not error:
            self.error = 'This is not a valid email address.'



class IsNumeric(Regex):
    """ Regex convenience derivative class used to determine if given field value is numeric-only. """

    def __init__(self, error = None, pass_on_blank = False):
        super(IsNumeric, self).__init__(r'^[0-9]*$', error, pass_on_blank)
        if not error:
            self.error = 'This is not a number.'



class IsAlpha(Regex):
    """ Regex convenience derivative class used to determine if given field value is alpha-only. """

    def __init__(self, error = None, pass_on_blank = False):
        super(IsAlpha, self).__init__(r'^[a-zA-Z]*$', error, pass_on_blank)
        if not error:
            self.error = 'This is not an alpha-only string.'



class IsAlphaNumeric(Regex):
    """ Regex convenience derivative class used to determine if given field value is alpha-numeric. """

    def __init__(self, error = None, pass_on_blank = False):
        super(IsAlphaNumeric, self).__init__(r'^[a-zA-Z0-9]*$', error, pass_on_blank)
        if not error:
            self.error = 'This is not an alpha-numeric string.'



class IsRequired(Rule):
    """ Used to determine if given field is empty. """

    def __init__(self, error = None, pass_on_blank = False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """

        super(IsRequired, self).__init__(error, pass_on_blank)

    def run(self, field_value):
        """ Determines if field_value value is empty.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if self.pass_on_blank and not field_value.strip():
            return True

        if not field_value:
            if not self.error:
                self.error = 'This field requires a value.'
            return False
        return True



class IsLength(Rule):
    """ Used to determine whether the given associated field value's character length equals
    the given maximum amount. """

    length = None
    """ Absolute maximum character length. """

    strip = False
    """ Determines whether to strip whitespace from either side of the given field value. """

    def __init__(self, length, strip = False, error = None, pass_on_blank = False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        length int         -- Absolute maximum character length.
        strip bool         -- Used to strip whitespace from the given field value. (optional)
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """

        super(IsLength, self).__init__(error, pass_on_blank)
        self.length = int(length)
        self.strip = bool(strip)

    def run(self, field_value):
        """ Determines if field_value character length equal self.length.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if self.pass_on_blank and not field_value.strip():
            return True

        if len((field_value.strip() if self.strip else field_value)) != self.length:
            if not self.error:
                self.error = "String `%s` length does not equal `%d`" % (field_value, self.length)
            return False
        return True



class IsLengthBetween(Rule):
    """ Used to determine whether the given associated field value's character length is
    within the given range. """

    minimum = 0
    """ Absolute minimum character length. """

    maximum = 0
    """ Absolute maximum character length. """

    strip = False
    """ Determines whether to strip whitespace from either side of the given field value. """

    def __init__(self, minimum, maximum, **kwargs):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        minimum int        -- Absolute minimum character length.
        max int            -- Absolute maximum character length.
        strip bool         -- Used to strip whitespace from the given field value. (optional)
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        super(IsLengthBetween, self).__init__(kwargs.get('error', None), kwargs.get('pass_on_blank', False))
        self.minimum = int(minimum)
        self.maximum = int(maximum)
        self.strip = kwargs.get('strip', False)

    def run(self, field_value):
        """ Determines if field_value character length is between self.minimum and self.maximum.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if self.pass_on_blank and not field_value.strip():
            return True

        if self.minimum <= len((field_value.strip() if self.strip else field_value)) <= self.maximum:
            return True

        if not self.error:
            self.error = "String `%s` length is not within `%d` and `%d`" % (field_value, self.minimum, self.maximum)

        return False



class IsInList(Rule):
    """ Used to determine if the associated field's value exists within the specified list. """

    given_list = list()
    """ A list that contains items that may, or may not, include the given field value. """

    strip = False
    """ Determines whether to strip whitespace from either side of the given field value. """

    def __init__(self, given_list, strip = False, error = None, pass_on_blank = False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        given_list list          -- List containing values to evaluate.
        strip bool         -- Used to strip whitespace from the given field value. (optional)
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """

        super(IsInList, self).__init__(error, pass_on_blank)
        self.given_list = given_list
        self.strip = strip

    def run(self, field_value):
        """ Checks if field_value is included within self.given_list.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if self.pass_on_blank and not field_value.strip():
            return True

        if (field_value.strip() if self.strip else field_value) not in self.given_list:
            if not self.error:
                self.error = "Value of `%s` is not within the list" % field_value
            return False
        return True



class IsType(Rule):
    """ Rule that compares the associated field's value against a specified data type. """

    asserted_type = None
    """ The type to compare the field value against. """

    def __init__(self, asserted_type, error = None, pass_on_blank = False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        asserted_type mixed -- The type to compare the field value against.
        error str           -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool  -- Pass through as success if field value is blank. (optional)
        """

        super(IsType, self).__init__(error, pass_on_blank)
        self.asserted_type = asserted_type

    def run(self, field_value):
        """ Compares field_value against self.asserted_type.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """

        if self.pass_on_blank and not field_value.strip():
            return True

        if not isinstance(field_value, self.asserted_type):
            if not self.error:
                self.error = "Type of `%s` is not of type `%s`" % (type(field_value), self.asserted_type)
            return False
        return True