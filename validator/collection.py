# -*- coding: utf-8 -*-
import field

class Collection(object):
    """ Contains a list of fields and applies assocated rules against them. """
    def __init__(self):
        """ Constructor that instantiates a class instance and properties. """
        self.fields = []
        self.collated_results = []

    def append(self, _field):
        """ Attaches an instance of class Field to the current instance of this collection

        Keyword arguments:
        field object -- Instance of class Field to apply to this collection.
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

    def __iter__(self):
        """ Returns generator to iterate through assigned fields. """
        for rule in self.fields:
            yield rule

    def __len__(self):
        """ Implements built-in len() to return number of assigned fields. """
        return len(self.fields)

    def __getitem__(self, i):
        """ Allows for self[key] access. Will raise IndexError if out of range. """
        return self.fields[i]

    def results(self):
        """ Returns the collated results for the current collection instance. """
        return self.collated_results

    def form(self):
        """ Returns a dict representing the current form in field:value pairs. """
        return {
            field.title:field.value
            for field in self.fields
        }

    def errors(self):
        """ Returns a dict containing only a map of fields with any 
        corresponding errors or None if all rules passed.
        """
        return {
            f['field']:f['errors']
            for f in self.collated_results
            if f['errors']
        } or None

    def run(self, return_collated_results = False):
        """ Iterates through all associated Fields and applies all attached Rules. Depending on 'return_collated_results',
        this method will either return True (all rules successful), False (all, or some, rules failed) or a dictionary list
        containing the collated results of all Field Rules.

        Keyword arguments:
        return_collated_results bool -- Returns dictionary list of Field Rule collated results instead of True or False.
        """
        self.collated_results = []

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