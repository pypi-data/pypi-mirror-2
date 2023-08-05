"""Definition of the Recaptchaed Content content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from collective.recaptchawidget import recaptchawidgetMessageFactory as _

from collective.recaptchawidget.interfaces import IRecaptchaedContent
from collective.recaptchawidget.config import PROJECTNAME
from collective.recaptchawidget.field import CaptchaField

RecaptchaedContentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        'Text',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Text"),
            description=_(u"Field description"),
        ),
        required=True,
    ),

    CaptchaField(
        'captcha',
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

RecaptchaedContentSchema['title'].storage = atapi.AnnotationStorage()
RecaptchaedContentSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(RecaptchaedContentSchema, moveDiscussion=False)


class RecaptchaedContent(base.ATCTContent):
    """Just some content type with a captcha"""
    implements(IRecaptchaedContent)

    meta_type = "RecaptchaedContent"
    schema = RecaptchaedContentSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    Text = atapi.ATFieldProperty('Text')

atapi.registerType(RecaptchaedContent, PROJECTNAME)
