import zc.ajaxform.application
import zc.ajaxform.interfaces
import zc.ajaxform.widgets
import zc.ajaxform.form
import zope.component
import zope.interface
import zope.formlib
import zope.schema

class IAddress(zope.interface.Interface):

    street = zope.schema.TextLine(
        title = u"Street",
        description = u"The street",
        )

    city = zope.schema.TextLine(
        title = u"City",
        description = u"The city",
        )

    awesomeness = zope.schema.Int(
        title = u"Awesomeness",
        description = u"The awesomeness on a scale of 1 to 10",
        min = 1,
        max = 10,
        )


class Pets(zc.sourcefactory.basic.BasicSourceFactory):

    def getValues(self):
        return (u'Dog', u'Cat', u'Fish')


class Pet(zope.schema.TextLine):
    """A textline representing a pet.

    This is just a textline, but we also have a source of common pets that
    the user can choose from.
    """

class IPerson(zope.interface.Interface):

    first_name = zope.schema.TextLine(
        title = u"First name",
        description = u"Given name.",
        default= u'Happy'
        )

    last_name = zope.schema.TextLine(
        title = u"Last name",
        description = u"Family name.",
        default= u'Camper'
        )

    favorite_color = zope.schema.TextLine(
        title = u"Favorite color",
        required = False,
        default= u'Blue'
        )

    age = zope.schema.Int(
        title = u"Age",
        description = u"Age in years",
        min = 0,
        max = 200,
        default= 23
        )

    happy = zope.schema.Bool(
        title = u"Happy",
        description = u"Are they happy?",
        default= True
        )

    pet = Pet(
        title=u'Pet',
        description=u'This person\'s best friend.',
        required=False,
        )

    temperment = zope.schema.Choice(
        title = u"Temperment",
        description = u"What is the person like?",
        values = ['Nice', 'Mean', 'Ornery', 'Right Neighborly'],
        default = u'Right Neighborly'
        )

    weight = zope.schema.Decimal(
        title = u"Weight",
        description = u"Weight in lbs?"
        )

    description = zope.schema.Text(
        title = u"Description",
        description = u"What do they look like?",
        default = u'10ft tall\nRazor sharp scales.'
        )

    secret = zope.schema.TextLine(
        title = u"Secret Key",
        description = u"Don't tell anybody",
        default = u'5ecret sauce'
        )

    siblings = zope.schema.Int(
        title = u"Siblings",
        description = u"Number of siblings",
        min = 0,
        max = 8,
        default = 1
        )

    addresses = zope.schema.List(
        title = u'Addresses',
        description = u"All my wonderful homes",
        value_type = zope.schema.Object(schema=IAddress),
        default= [{'street':'123 fake street',
                   'city': 'fakeville',
                   'awesomeness': '9'},
                  {'street':'345 false street',
                   'city': 'falsetown',
                   'awesomeness': '9001'}
                 ]
        )

    other = zope.schema.Text(
        title = u"Other",
        description = u"Any other notes",
        default = u"I've got a magic toenail"
        )

class Person:

    zope.interface.implements(IPerson)

    def __init__(self, first_name, last_name, favorite_color, age, happy,
                 pet, temperment, weight, description, secret, siblings,
                 addresses, other):
        self.first_name = first_name
        self.last_name = last_name
        self.favorite_color = favorite_color
        self.age = age
        self.happy = happy
        self.pet = pet
        self.temperment = temperment
        self.weight = weight
        self.description = description
        self.secret = secret
        self.siblings = siblings
        self.addresses = addresses
        self.other = other


class FormExample(zc.ajaxform.application.Application):

    resource_library_name = None

    class ExampleForm(zc.ajaxform.form.Form):

        leftFields = ('first_name', 'last_name', 'age', 'other')
        form_fields = zope.formlib.form.Fields(IPerson)
        form_fields['secret'].custom_widget = zc.ajaxform.widgets.Hidden
        form_fields['siblings'].custom_widget = zc.ajaxform.widgets.NumberSpinner

        @zope.formlib.form.action("Register")
        def register(self, action, data):
            person = Person(**data)
            return dict(
                data = data,
                self_class_name = self.__class__.__name__,
                self_app_class_name = self.app.__class__.__name__,
                self_context_class_name = self.context.__class__.__name__
                )


class PetWidget(zc.ajaxform.widgets.ComboBox):
    zope.component.adapts(
        Pet,
        zc.ajaxform.interfaces.IAjaxRequest)
    zope.interface.implements(
        zc.ajaxform.interfaces.IInputWidget)

    def __init__(self, context, request):
        super(PetWidget, self).__init__(context, Pets(), request)
