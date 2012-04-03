#!/usr/bin/env python

""" Validator Core Module

Contains all core classes required for the validator to function properly.
"""

class Rule(object):
  """ Base abstract class representing a "rule". All defined rules must be derived from this class. """

  error = None
  """ User-defined error message for a failed rule. """

  def __init__(self, error = None, *args, **kwargs):
    """ Constructor that instantiates a class instance and properties.

    Keyword arguments:
    error str -- A user-defined error messaged for a failed rule. (optional)
    """

    super(Rule, self).__init__()
    self.error = error


  def run(self, *args, **kwargs):
    """ Invoked once a defined rule is ready to be validated. """

    raise NotImplementedError, 'This method cannot be accessed directly'


class Field(object):
  """ Class representing a "field". """

  rules = []
  """ List containing instances of class Rule associated with this field. """

  title = ''
  """ The title of this field. """

  value = ''
  """ The value associated with this field. """

  def __init__(self, title, value):
    """ Constructor that instantiates a class instance and properties.

    Keyword arguments:
    title str -- The title of this field.
    value str -- The value associated with this field.
    """

    super(Field, self).__init__()
    self.rules = []
    self.title = title
    self.value = value


  def append(self, rule):
    """ Attaches an instance of class Rule to the current instance of this Field

    Keyword arguments:
    rule object -- Instance of class Rule to apply to this field.
    """

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
    """ Iterates through all associated rules, executes them and collects the results. """
    errors = []
    for rule in self.rules:
      if not rule.run(self.value):
        errors.append(rule.error)
    return False if errors else True, errors


class Validator(object):
  """ Responsible for applying rules against the specified fields. """

  fields = []
  """ List containing instances of class Field associated with this validator. """

  collated_results = []
  """ List containing validation results of each field and associated rule. """

  def __init__(self):
    """ Constructor that instantiates a class instance and properties. """

    super(Validator, self).__init__()
    self.fields = []
    self.collated_results = []


  def append(self, field):
    """ Attaches an instance of class Field to the current instance of this Validator

    Keyword arguments:
    field object -- Instance of class Field to apply to this Validator.
    """

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
    """ Returns the collated results for the current Validator instance. """

    return self.collated_results


  def run(self, return_collated_results = False):
    """ Iterates through all associated Fields and applies all attached Rules. Depending on 'return_collated_results',
    this method will either return True (all rules successful), False (all, or some, rules failed) or a dictionary list
    containing the collated results of all Field Rules.

    Keyword arguments:
    return_collated_results bool -- Returns dictionary list of Field Rule collated results instead of True or False.
    """

    passed = True
    for field in self.fields:
      result, errors = field.run()

      results = {
        'field': field.title,
        'value': field.value,
        'passed': result
      }

      if errors:
        passed = False
        results['errors'] = errors

      self.collated_results.append(results)

    if return_collated_results:
      return self.collated_results
    return passed