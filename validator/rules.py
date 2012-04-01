from validator.core import Rule

class Matches(Rule):
	def __init__(self, value, error = None):
		super(Matches, self).__init__(value, error)


	def run(self, matched):
		if self.value is not matched:
			return False
		return True