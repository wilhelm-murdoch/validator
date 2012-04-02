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



class IsNumeric(Regex):
	def __init__(self, error = None):
		super(IsNumeric, self).__init__(r'^[0-9]+$', error)



class IsAlpha(Regex):
	def __init__(self, error = None):
		super(IsAlpha, self).__init__(r'^[a-zA-Z]+$', error)



class IsAlNum(Regex):
	def __init__(self, error = None):
		super(IsAlNum, self).__init__(r'^[a-zA-Z0-9]+$', error)



class IsRequired(Rule):
	pass



class IsWithinRange(Rule):
	pass



class IsType(Rule):
	valid = ['bool', 'str', 'list', 'dict', 'object', 'tuple']
	type = ''
	def __init__(self, error = None):
		super(IsType, self).__init__(type, error)
		self.type = type

	def run(self, field_value):
		pass
