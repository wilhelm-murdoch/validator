# -*- coding: utf-8 -*-
import rule
import re

class Matches(rule.Rule):
    """ Simple rule used to determine whether one value matches another. Commonly used
    for password confirmation. """
    def __init__(self, match, error=None, pass_on_blank=False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        match str          -- The value to compare against the associated field's value.
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        if not error:
            error = "Values `{}` and `{}` do not match."

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
            self.error = self.error.format(field_value, self.match)
            return False
        return True


class Regex(rule.Rule):
    """ Applies a regular expression to a given field value. """
    def __init__(self, expression, error=None, pass_on_blank=False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        expression str     -- The regular expression to apply to the given field.
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        if not error:
            error = "Could not match `{}` with expression `{}`"
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
                self.error = self.error.format(field_value, self.expression)
                return False
        except Exception, e:
            raise ValueError("Expression `{}` failed with the following error: {}".format(self.expression, e))
        return True


class IsEmail(Regex):
    """ Regex convenience derivative class used to determine if given field value is a
    valid email address. """
    def __init__(self, error=None, pass_on_blank=False):
        if not error:
            error = 'This is not a valid email address.'
        super(IsEmail, self).__init__(r'^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', error, pass_on_blank)


class IsNumeric(Regex):
    """ Regex convenience derivative class used to determine if given field value is numeric-only. """
    def __init__(self, error=None, pass_on_blank=False):
        if not error:
            error = 'This is not a number.'
        super(IsNumeric, self).__init__(r'^[0-9]*$', error, pass_on_blank)


class IsAlpha(Regex):
    """ Regex convenience derivative class used to determine if given field value is alpha-only. """
    def __init__(self, error=None, pass_on_blank=False):
        if not error:
            error = 'This is not an alpha-only string.'
        super(IsAlpha, self).__init__(r'^[a-zA-Z]*$', error, pass_on_blank)


class IsAlphaNumeric(Regex):
    """ Regex convenience derivative class used to determine if given field value is alpha-numeric. """
    def __init__(self, error=None, pass_on_blank=False):
        if not error:
            error = 'This is not an alpha-numeric string.'
        super(IsAlphaNumeric, self).__init__(r'^[a-zA-Z0-9]*$', error, pass_on_blank)


class IsRequired(rule.Rule):
    """ Used to determine if given field is empty. """
    def __init__(self, error=None, pass_on_blank=False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        if not error:
            error = 'This field requires a value.'
        super(IsRequired, self).__init__(error, pass_on_blank)

    def run(self, field_value):
        """ Determines if field_value value is empty.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """
        if self.pass_on_blank and not field_value.strip():
            return True

        if not field_value:
            return False
        return True


class IsLength(rule.Rule):
    """ Used to determine whether the given associated field value's character length equals
    the given maximum amount. """
    def __init__(self, length, strip = False, error=None, pass_on_blank=False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        length int         -- Absolute maximum character length.
        strip bool         -- Used to strip whitespace from the given field value. (optional)
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        if not error:
            error = "String `{}` length does not equal `{}`"
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
            self.error = self.error.format(field_value, self.length)
            return False
        return True


class IsLengthBetween(rule.Rule):
    """ Used to determine whether the given associated field value's character length is
    within the given range. """
    def __init__(self, minimum, maximum, **kwargs):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        minimum int        -- Absolute minimum character length.
        max int            -- Absolute maximum character length.
        strip bool         -- Used to strip whitespace from the given field value. (optional)
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        if not kwargs.get('error', None):
            kwargs['error'] = "String `{}` length is not within `{}` and `{}`"
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

        self.error = self.error.format(field_value, self.minimum, self.maximum)
        return False


class IsInList(rule.Rule):
    """ Used to determine if the associated field's value exists within the specified list. """
    def __init__(self, given_list, strip = False, error=None, pass_on_blank=False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        given_list list          -- List containing values to evaluate.
        strip bool         -- Used to strip whitespace from the given field value. (optional)
        error str          -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool -- Pass through as success if field value is blank. (optional)
        """
        if not error:
            error = "Value of `{}` is not within the list"
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
            self.error = self.error.format(field_value)
            return False
        return True


class IsType(rule.Rule):
    """ Rule that compares the associated field's value against a specified data type. """
    def __init__(self, asserted_type, error=None, pass_on_blank=False):
        """ Constructor that instantiates a class instance and properties.

        Keyword arguments:
        asserted_type mixed -- The type to compare the field value against.
        error str           -- A user-defined error messaged for a failed rule. (optional)
        pass_on_blank bool  -- Pass through as success if field value is blank. (optional)
        """
        if not error:
            error = "Type of `{}` is not of type `{}`"
        super(IsType, self).__init__(error, pass_on_blank)
        self.asserted_type = asserted_type

    def run(self, field_value):
        """ Compares field_value against self.asserted_type.

        Keyword arguments:
        field_value str -- the value of the associated field to compare
        """
        if self.pass_on_blank and not field_value.strip():
            return True

        if not isinstance(field_value, type(self.asserted_type)):
            self.error = self.error.format(type(field_value), self.asserted_type)
            return False
        return True