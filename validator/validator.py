# -*- coding: utf-8 -*-
import field

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


    def append(self, _field):
        """ Attaches an instance of class Field to the current instance of this Validator

        Keyword arguments:
        field object -- Instance of class Field to apply to this Validator.
        """

        if isinstance(_field, list):
            for f in _field:
                if not isinstance(f, field.Field):
                    raise TypeError('parameter :field must be list of class Field instances')
                self.fields.append(f)
            return self
        if not isinstance(_field, field.Field):
            raise TypeError('parameter :field must be instance of class Field')
        self.fields.append(_field)
        return self


    def results(self):
        """ Returns the collated results for the current Validator instance. """

        return self.collated_results


    def form(self):
        """ Returns a dictionary/object representing the current form. """
        return {
            field.title:field.value
            for field in self.fields
        }


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
                'passed': result,
                'errors': None
            }

            if errors:
                passed = False
                results['errors'] = errors

            self.collated_results.append(results)

        if return_collated_results:
            return self.collated_results
        return passed