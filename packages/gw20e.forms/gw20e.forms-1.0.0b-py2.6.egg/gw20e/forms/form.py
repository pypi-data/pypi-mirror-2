from zope.interface import implements
from interfaces import IForm


class FormValidationError(Exception):

    def __init__(self, errors={}):
        Exception.__init__(self)
        self._errors = errors


    def __repr__(self):

        print "FormValidationError: %s" % self._errors


    @property
    def errors(self):

        return self._errors
    

    def addError(self, fieldId, error):

        if not self._errors.has_key():
            self._errors[fieldId] = []
            
        self._errors[fieldId].append(error)



class Form:
 
    """ Basic form implementation class. This class basically holds a
    data object, a model and a view.
    """

    implements(IForm)


    def __init__(self, id, data, model, view, submission):

        """ Initialize the form, using the given data, model and view.
        """

        self.id = id
        self.data = data
        self.model = model
        self.view = view
        self.submission = submission


    def render(self):

        return self.view.render(self)


    def validate(self, fields=None):

        """ Validate the form. If this fails, an FormValidationError is raised,
        that holds the errors encountered in an associative array, using the
        node id as key, and an array of error messages as value.

        Validation works as follows:
         * check for requiredness for each field. If a field is required, and
           not set, this is an error
         * check for constraints on the field. If any are failed to meet,
           this is an error
        
        """
        
        errors = {}
        value = None


        if not fields:

            fields = self.data.getFields()
            

        for field in fields:

            field_errors = []

            try:           
                value = self.data[field]
            except:
                pass
                
            # Requiredness
            if self.isEmpty(value) and self.model.isRequired(field, self.data):

                field_errors.append("required")

            # check datatype
            if value:
                try:
                    self.model.checkDatatype(field, value)
                except:
                    field_errors.append("datatype")

            # Constraint checking...
            if not self.model.meetsConstraint(field, self.data):
                field_errors.append("constraint")

            if field_errors:
                errors[field] = field_errors

        if errors:
            raise FormValidationError(errors)
        else:
            return True


    def isEmpty(self, value):
        
        """ Check whether value is empty """
        
        if value is None or value == "":
            
            return True
        
        return False
