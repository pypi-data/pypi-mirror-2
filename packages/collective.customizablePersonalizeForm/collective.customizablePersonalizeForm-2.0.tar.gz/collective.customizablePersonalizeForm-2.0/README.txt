
.. contents::

- Questions and comments to Quadra Informatique <plone@quadra-informatique.fr>
- Report bugs to Quadra Informatique <maintenance.plone@quadra-informatique.fr>

Introduction
============

This package was created after encountering a problem with the plone.app.users.userdataschema.IUserDataSchemaProvider utilty override.
As this utility is unnamed, you can override it only once in all packages. We had to add extra fields on our personal-information form from various packages, so this package was created with the idea of managing multiple sources overrides of the personal-information form and properties.

This eggs allows to override as many times as you want the personal preferences of your users by adding extra fields by using adapters.
By adding extra fields, you can specify your own getters & setters if you don't want your field to be manage as a user property.
You'll also be able to add comptabile widgets for the personal preferences' form fields.

The docs directory contains all necessary steps about server configuration
before to install this egg. These documents can be distributed separately under
the specified license in each of them.

These package was initiated by Quadra Informatique <plone@quadra-informatique.fr>.

How-to
======

There are three interfaces you need to know:

collective.customizablePersonalizeForm.adapters.interfaces.IExtendedUserDataSchema(Interface):

    def getSchema(self,):

collective.customizablePersonalizeForm.adapters.interfaces.IExtendedUserDataPanel(Interface):
    
    def getProperties(self,):

collective.customizablePersonalizeForm.adapters.interfaces.IExtendedUserDataWidgets(Interface):

    def getWidgets(self,):

An adapter providing the IExtendedUserDataSchema allows to add additional fields by returning an Interface through its getSchema method.

Carefull !
If you ever add a field on your form, you'll also need to declare a property with the same name as your field, allowing you to get and set your property.
That's why we use IExtendedUserDataPanel. An adapter providing this interface will return a list of strings through the getProperties method. 
These strings are the names of the fields provided by your custom interface, like 'portrait' or 'fullname'.
By default the getters and setters of your fields will use Plone's member.getProperty and member.setProperty methods, using the memberdata to store the values. If you ever need to use your own getters and setters, you can return a dict instead of the name of your field, using this format:

 {'name' : 'your_field_name', 'getter': your_own_getter_method, 'setter': your_own_setter_method}

Simple Override Example
-----------------------

A simple interface providing our field:

class ITestAdditionalDataSchema(Interface):

    test_field = schema.Bool(
        title=_(u'label_test_field_title', default=u'Test field'),
        description=_(u'label_test_field_description', default=u''),
        required=False,
        )

A simple adapter that adapts the context and request, returning our interface

class TestSchemaAdapter(object):
    adapts(object, IBrowserRequest)
    implements(IExtendedUserDataSchema)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getSchema(self):
        return ITestAdditionalDataSchema

Now we create an adapter that will declare a 'test_field' property, we didn't specify a getter and setter so this property will act as a memberdata property (be sure to declare it via memberdata_properties.xml)

class TestPropertiesAdapter(object):
    adapts(object, IBrowserRequest)
    implements(IExtendedUserDataPanel)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getProperties(self):
        return ['test_field']

Let's susbscribe to the collective.customizablePersonalizeForm's interfaces to provide the personal-information form with our field

    <adapter factory=".adapters.TestSchemaAdapter"
             name="test.ExtraField"/>

    <adapter factory=".adapters.TestPropertiesAdapter"
             name="test.ExtraProperties"/>

Congratulations, a simple boolean field named 'test_field' should now be displayed in your form.

Custom Widgets
--------------

You may want to use a widget for your field. It can be done through the IExtendedUserDataWidgets interface.
All you have to do is mapping a field id with a valid custom_widget factory like the following example.

class TestWidgetAdapter(object):
    adapts(object, IBrowserRequest)
    implements(IExtendedUserDataWidgets)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getWidgets(self):
        return [{'field': 'test_field', 'factory' : CheckBoxWidget},
               ]

    <adapter factory=".adapters.TestWidgetAdapter"
             name="test.ExtraWidgets"/>

Your test_field will now use the widget factory you declared in the getWidgets method. You can also override the default Plone fields widgets using this method if you ever need to.

