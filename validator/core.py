class Rule(object):
	def __init__(self, value, error = None):
		super(Rule, self).__init__()
		self.value = value
		self.error = error


	def run(self, *args, **kwargs):
		raise NotImplementedError, 'This method cannot be accessed directly'

class Field(object):
	def __init__(self, title, value):
		super(Field, self).__init__()
		self.rules = []
		self.title = title
		self.value = value


	def append(self, rule):
		if isinstance(rule, list):
			for r in rule:
				if not isinstance(r, Rule):
					raise TypeError, 'parameter :rule must be list of class Rule instances'
				self.rules.append(r)
			return self
		elif not isinstance(rule, Rule):
			raise TypeError, 'parameter :rule must be instance of class Rule'
		self.rules.append(rule)
		return self


	def run(self):
		errors = []
		for rule in self.rules:
			if not rule.run(self.value):
				errors.append(rule.error)
		return False if errors else True, errors

class Validator(object):
	def __init__(self):
		super(Validator, self).__init__()
		self.fields = []
		self.collated_results = []


	def append(self, field):
		if isinstance(field, list):
			for f in field:
				if not isinstance(f, Field):
					raise TypeError, 'parameter :field must be list of class Field instances'
				self.fields.append(f)
			return self
		if not isinstance(field, Field):
			raise TypeError, 'parameter :field must be instance of class Field'
		self.fields.append(field)
		return self


	def results(self):
		return self.collated_results


	def run(self, return_collated_results = False):
		passed = True
		for field in self.fields:
			result, errors = field.run()
			self.collated_results.append({'field': field.title, 'passed': result, 'errors': errors})
			if errors:
				passed = False
		if return_collated_results:
			return self.collated_results
		return passed

