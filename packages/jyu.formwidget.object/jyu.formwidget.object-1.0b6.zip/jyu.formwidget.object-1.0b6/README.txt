schema.Object made simple
=========================

This package introduces an experimental proof-of-concept support for
object-fields (*zope.schema.Object*) on z3c.form and Plone for a
use-case where one desires to save schema based hierarchical data on
objects.

I can't say, why anyone would like to do that (instead of mapping data
to containers and items), but I hope this package provides examples,
how to make object-fields work with *plone.autoform* and Plone's
KSS-validation.

This package

* provides *ISubformFactory* for object-widget within *IAutoExtensibleForm*
* implements simple Plone-style *input* and *display* widgets for object-field
* introduces refactored KSS-validation integration with support for object-field
* monkeypatches ``plone.z3cform``\'s widget traversal to support object-widgets
* overrides default *DataConverter* for *ObjectWidget*\'s with a less invasive one
* provides a simple abstract factory class to store object-fields'
  values as *SimpleItem*-properties.

Note that this package relies on ``plone.app.z3cform`` and
*IPloneFormLayer* it registers.

Example of Use
==============

At first we define a simple schema we'd like to re-use as a part of other schemas::

  from zope import schema
  from zope.interface import invariant, Invalid

  from plone.directives import form

  from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
  _= ZopeMessageFactory("my.package")


  class StartBeforeEnd(Invalid):
      __doc__ = _(u"The start or end date is invalid")


  class IPeriod(form.Schema):
      start = schema.Date(
          title=_(u"period_start_label",
                  default=u"Period began"),
          required=True
          )

      end = schema.Date(
          title=_(u"period_end_label",
                  default=u"Period ended"),
          required=True
          )

      @invariant
      def validateStartEnd(data):
          if data.start is not None and data.end is not None:
              if data.start > data.end:
                  raise StartBeforeEnd(\
                      _(u"The start date must be before the end date."))

Then we define the main schema, which re-uses the first schema::

  class IWorkPeriod(form.Schema):
      title = schema.TextLine(
          title=_(u"work_title_label",
                  default=u"Title"),
          required=True
          )
      description = schema.TextLine(
          title=_(u"work_description_label",
                  default=u"Description"),
          required=False
          )
      period = schema.Object(
          title=_(u"work_period",
                  default=u"Period"),
          schema=IPeriod,
          required=True
          )

Finally, we register an object factor, which creates *SimpleItem*
matching our schema for *z3c.form* to validate and store as a
property of the actual object being created or edited::

  from five import grok

  from zope.interface import Interface

  from z3c.form.interfaces import IObjectFactory

  from jyu.formwidget.object.factory import AbstractBaseFactory

  from my.package.schemas import IPeriod


  class PeriodFactory(AbstractBaseFactory, grok.MultiAdapter):
      grok.provides(IObjectFactory)
      grok.name("my.package.schemas.IPeriod")
      grok.adapts(Interface, Interface, Interface, Interface)

To be able to test this, you should, of course, also define and
register a new content type based on the main schema (e.g. with
Dexterity).

Known Problems
==============

It appeared not to be a very good idea to register a custom
datamanager for (Interface, IObject), because many products provide
fields inherited from IObject, but still expect AttributeField as
datamanager.

The following *zcml* can be used as an example to re-register
AttributeField-datamanager explicitly for those fields that are
inherited from IObject, but expect AttributeField-datamanager::

  <configure
     xmlns="http://namespaces.zope.org/zope"
     xmlns:zcml="http://namespaces.zope.org/zcml"
    <configure zcml:condition="installed plone.app.textfield">
      <adapter
         provides="z3c.form.interfaces.IDataManager"
         for="zope.interface.Interface
              plone.app.textfield.interfaces.IRichText"
         factory="z3c.form.datamanager.AttributeField"
         />
    </configure>
    <configure zcml:condition="installed plone.namedfile">
      <adapter
         provides="z3c.form.interfaces.IDataManager"
         for="zope.interface.Interface
              plone.namedfile.interfaces.INamedImageField"
         factory="z3c.form.datamanager.AttributeField"
         />
      <adapter
         provides="z3c.form.interfaces.IDataManager"
         for="zope.interface.Interface
              plone.namedfile.interfaces.INamedFileField"
         factory="z3c.form.datamanager.AttributeField"
         />
      <configure zcml:condition="installed plone.app.blob">
        <adapter
           provides="z3c.form.interfaces.IDataManager"
           for="zope.interface.Interface
                plone.namedfile.interfaces.INamedBlobImageField"
           factory="z3c.form.datamanager.AttributeField"
           />
        <adapter
           provides="z3c.form.interfaces.IDataManager"
           for="zope.interface.Interface
                plone.namedfile.interfaces.INamedBlobFileField"
           factory="z3c.form.datamanager.AttributeField"
           />
      </configure>
    </configure>
