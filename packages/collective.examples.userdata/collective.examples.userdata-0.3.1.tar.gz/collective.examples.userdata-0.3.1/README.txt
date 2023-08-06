Introduction
============

Since Plone 4, the registration form for new users is a Zope formlib_ form,
defined in plone.app.users_. plone.app.users allows the site administrator to
select fields from this schema to appear on the registration form.

This product aims to show how you could extend or modify the default schema
provided by plone.app.users, and add new fields to the registration form.

How it works
============

Overriding the default schema 
-----------------------------

The default schema is defined in plone.app.users, and is provided by a utility.
We override this utility in the file 
``profiles/default/componentregistry.xml``::

    <utility
      interface="plone.app.users.userdataschema.IUserDataSchemaProvider"
      factory="collective.examples.userdata.userdataschema.UserDataSchemaProvider"

Our ``userdataschema.py`` contains::

    from plone.app.users.userdataschema import IUserDataSchemaProvider

    class UserDataSchemaProvider(object):
        implements(IUserDataSchemaProvider)

        def getSchema(self):
            """
            """
            return IEnhancedUserDataSchema

And, also in ``userdataschema.py``, we subclass the default schema::

    from plone.app.users.userdataschema import IUserDataSchema

    class IEnhancedUserDataSchema(IUserDataSchema):
        """ Use all the fields from the default user data schema, and add various
        extra fields.
        """

Adding fields to the schema
---------------------------

The "Country" field
~~~~~~~~~~~~~~~~~~~

We can now add a schema field to our schema class::

    class IEnhancedUserDataSchema(IUserDataSchema):
        # ...
        country = schema.TextLine(
            title=_(u'label_country', default=u'Country'),
            description=_(u'help_country',
                          default=u"Fill in which country you live in."),
            required=False,
            )    

Various other fields
~~~~~~~~~~~~~~~~~~~~

There are various other extra fields with which you could extend your users'
profile. In ``userdataschema.py`` you will find examples for:

- a Date field (``birthdate``)
- a Boolean field (``newsletter``)
- a Choice field (``gender``)

The "Accept Terms" field
~~~~~~~~~~~~~~~~~~~~~~~~

A special case is the ``accept`` field. This is a Boolean field which is
required for signup. We implement it by adding a ``constraint`` to the schema::

    def validateAccept(value):
        if not value == True:
            return False
        return True

    class IEnhancedUserDataSchema(IUserDataSchema):
        # ...
        accept = schema.Bool(
            title=_(u'label_accept', default=u'Accept terms of use'),
            description=_(u'help_accept',
                          default=u"Tick this box to indicate that you have found,"
                          " read and accepted the terms of use for this site. "),
            required=True,
            constraint=validateAccept,
            )

Because this field can be ignored once registration is complete, we don't add
it to the memberdata properties (see below).

Adding fields to the memberdata properties
------------------------------------------

In ``profiles/default/memberdata_properties.xml``, we add the fields that we
want to store as properties on the member. These are all the fields we defined,
except the "accept" field, which is wanted only for signup.

Default settings for registration fields
----------------------------------------

We can automatically select some fields to go on the registration form. The
fields we define in ``profiles/default/propertiestool.xml`` will be on the form
once the product is installed.

Of course, the site manager can modify this after installation.

Making added fields available on the Personal Information form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to see these properties in the Personal Information form
(`@@personal-information`), we need to take a few extra steps. We have to
override the default adapter which adapts a user object to a form. See the
plone.app.controlpanel_ documentation for a detailed explanation.

To override plone.app.users' default adapter, we put this in `overrides.zcml`::
    
  <adapter 
    provides=".userdataschema.IEnhancedUserDataSchema"
    for="Products.CMFCore.interfaces.ISiteRoot"
    factory=".adapter.EnhancedUserDataPanelAdapter"
    />

In `adapter.py`, we repeat (yes, this is unfortunate) the fields we defined in
the schema. For example, for the `firstname` field, we do this::

    class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
        """
        """
        def get_firstname(self):
            return self.context.getProperty('firstname', '')
        def set_firstname(self, value):
            return self.context.setMemberProperties({'firstname': value})
        firstname = property(get_firstname, set_firstname)

Hiding custom fields on @@personal-information view
---------------------------------------------------

(Supplied by Martijn Pieters on stackoverflow_, thanks to Gil Forcada for
drawing my attention to it on plone.org_)

Hiding a field from the ``@@personal-information`` form and only show it on the
``@@register`` form is not supported out-of-the-box, only the other way around.

You'll have to customize either the one or the other form to accomplish this:

* customize ``plone.app.users.browser.personalpreferences.UserDataPanel`` to
  remove your field 
* or provide a new version of
  ``plone.app.users.browser.register.RegistrationForm`` to add your field there.

Here's how I'd do it::

    plone.app.users.browser.personalpreferences import UserDataPanel

    class CustomizedUserDataPanel(UserDataPanel):
        def __init__(self, context, request):
            super(CustomizedUserDataPanel, self).__init__(context, request)
            self.form_fields = self.form_fields.omit('acceptTerms')

Note the ``.omit('acceptTerms')``, I had to guess at the name of your extra field.
You can then register this customized panel with ZCML against your theme
browser layer, or directly on your Plone site or a custom interface. Here I
take the easy way out and register it for the Plone site object::

    <browser:page
        for="Products.CMFPlone.Portal.PloneSite"
        name="personal-information"
        class=".mymodule.CustomizedUserDataPanel"
        permission="cmf.SetOwnProperties"
        />

This should work for both Plone 4.0 and 4.1, as this particular class did not change.

Rendering custom fields in ``author.cpt``
-----------------------------------------

(Thanks to Bill Freeman for pointing this out on plone.org_)

You need to also modify
``Products.PlonePAS.tools.membership.MembershipTool.getMemberInfo()`` if you want
to be able to render your new fields in, for example, ``author.cpt``.

Non-ASCII characters
--------------------

(Thanks to Imke Brandt for pointing this out on plone.org_)

If you try to use the product with member data with non-ASCII characters (e.g.
german 'umlaute'), you may run into encoding problems. To solve this, I
modified my ``adapter.py`` for every string field that may be affected by the
problem to look like this::

    def get_myfield(self):
        return unicode(self.context.getProperty('firstname', ''), 'utf-8')


.. _plone.app.users: http://pypi.python.org/pypi/plone.app.users
.. _formlib: http://pypi.python.org/pypi/zope.formliba
.. _plone.app.controlpanel: http://pypi.python.org/pypi/plone.app.controlpanel
.. _stackoverflow: http://stackoverflow.com/questions/6174506/hide-custom-fields-on-personal-information-view
.. _plone.org: http://plone.org/products/collective.examples.userdata
