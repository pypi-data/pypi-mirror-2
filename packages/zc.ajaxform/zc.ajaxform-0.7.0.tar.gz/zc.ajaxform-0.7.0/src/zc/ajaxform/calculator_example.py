import zc.ajaxform.application
import zope.exceptions

class Calculator(zc.ajaxform.application.Trusted,
                 zc.ajaxform.application.Application):

    resource_library_name = None

    @zc.ajaxform.application.jsonpage
    def about(self):
        return 'Calculator 1.0'

    @zc.ajaxform.application.jsonpage
    def operations(self):
        return ['add', "subtract"]

    @zc.ajaxform.application.jsonpage
    def value(self):
        return dict(value=getattr(self.context, 'calculator_value', 0))

    def do_add(self, value):
        value += getattr(self.context, 'calculator_value', 0)
        self.context.calculator_value = value
        return dict(value=value)
    
    @zc.ajaxform.application.jsonpage
    def add(self, value):
        if not isinstance(value, int):
            return dict(error="The value must be an integer!")
        return self.do_add(value)
    
    @zc.ajaxform.application.jsonpage
    def subtract(self, value):
        if not isinstance(value, int):
            raise zope.exceptions.UserError(
                "The value must be an integer!")
        return self.do_add(-value)

    @zc.ajaxform.application.jsonpage
    def noop(self):
        pass

    @zc.ajaxform.application.page
    def none(self):
        return "null"

    @zc.ajaxform.application.jsonpage
    def echo_form(self):
        def maybe_file(v):
            if hasattr(v, 'read'):
                return ("<File upload name=%r content-type=%r size=%r>"
                        % (v.filename, v.headers['content-type'], len(v.read()))
                        )
            else:
                return v
        
        return dict(
            (name, maybe_file(v))
            for (name, v) in self.request.form.items()
            )


    @zc.ajaxform.application.jsonpage
    def doh(self):
        raise TypeError("Doh!")
    
