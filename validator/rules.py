from validator.core import Rule
import re

class Matches(Rule):
    """ Simple rule used to determine whether one value matches another. Commonly used
	for password confirmation. """

	match = ''
	""" The value to compare against the associated field's value """

	def __init__(self, match, error = None):
		""" Constructor that instantiates a class instance and properties.

		Keyword arguments:
		match str -- The value to compare against the associated field's value.
		error str -- A user-defined error messaged for a failed rule. (optional)
		"""
		super(Matches, self).__init__(error)
		self.match = match


	def run(self, field_value):
		""" Invoked once a defined rule is ready to be validated.

		Keyword arguments:
		field_value str -- the value of the associated field to compare.
		"""

		if self.match != field_value:
			if not self.error:
				self.error = "Values `%s` and `%s` do not match." % (field_value, self.match)
			return False
		return True



class Regex(Rule):
	""" Applies a regular expression to a given field value. """

	expression = ''
	""" The regular expression to apply. """

	def __init__(self, expression, error = None):
		""" Constructor that instantiates a class instance and properties.

		Keyword arguments:
		expression str -- The regular expression to apply to the given field.
		error str      -- A user-defined error messaged for a failed rule. (optional)
		"""
		super(Regex, self).__init__(error)
		self.expression = expression


	def run(self, field_value):
		""" Invoked once a defined rule is ready to be validated.

		Keyword arguments:
		field_value str -- the value of the associated field to compare
		"""

		if not self.expression:
			raise ValueError, 'This rule requires a regular expression.'

		try:
			regex = re.compile(self.expression)

			if not regex.match(field_value):
				if not self.error:
					self.error = "Expression `%s` failed when applied to `%s`" % (self.expression, field_value)
				return False
		except Exception, e:
			raise ValueError, "Expression `%s` failed with the following error: %s" % (self.expression, e)
		return True



class IsEmail(Regex):
	def __init__(self, error = None):
		super(IsEmail, self).__init__(r'^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', error)
		if not error:
			self.error = 'This is not a valid email address.'



class IsNumeric(Regex):
	def __init__(self, error = None):
		super(IsNumeric, self).__init__(r'^[0-9]+$', error)
		if not error:
			self.error = 'This is not a number.'



class IsAlpha(Regex):
	def __init__(self, error = None):
		super(IsAlpha, self).__init__(r'^[a-zA-Z]+$', error)
		if not error:
			self.error = 'This is not an alpha-only string.'



class IsAlphaNumeric(Regex):
	def __init__(self, error = None):
		super(IsAlphaNumeric, self).__init__(r'^[a-zA-Z0-9]+$', error)
		if not error:
			self.error = 'This is not an alpha-numeric string.'


class IsRequired(Regex):
	def __init__(self, error = None):
		super(IsRequired, self).__init__(r'^.{1,}$', error)
		if not error:
			self.error = 'This field requires a value.'


class IsLength(Rule):
	length = None
	strip = False
	def __init__(self, length, strip = False, error = None):
		super(IsLength, self).__init__(error)
		self.length = int(length)
		self.strip = bool(strip)

	def run(self, field_value):
		if len((field_value.strip() if self.strip else field_value)) != self.length:
			if not self.error:
				self.error = "String `%s` length does not equal `%d`" % (field_value, self.length)
			return False
		return True



class IsLengthBetween(Rule):
	min = 0
	max = 0
	strip = False

	def __init__(self, min, max, strip = False, error = None):
		super(IsLengthBetween, self).__init__(error)
		self.min = int(min)
		self.max = int(max)
		self.strip = bool(strip)

	def run(self, field_value):
		if self.min <= len((field_value.strip() if self.strip else field_value)) <= self.max:
			return True
		if not self.error:
			self.error = "String `%s` length is not within `%d` and `%d`" % (field_value, self.min, self.max)
		return False


class IsInList(Rule):
	list = []
	strip = False
	def __init__(self, list, strip = False, error = None):
		super(IsInList, self).__init__(error)
		self.list = list
		self.strip = strip

	def run(self, field_value):
		if (field_value.strip() if self.strip else field_value) not in self.list:
			if not self.error:
				self.error = "Value of `%s` is not within the list" % field_value
			return False
		return True



class HasKeys(Rule):
	pass


class IsType(Rule):
	type = None
	def __init__(self, type, error = None):
		super(IsType, self).__init__(error)
		self.type = type

	def run(self, field_value):
		if not isinstance(field_value, self.type):
			if not self.error:
				self.error = "Type of `%s` is not type of `%s`" % (type(field_value), self.type)
			return False
		return True
