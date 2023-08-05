from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from collective.recaptchawidget import recaptchawidgetMessageFactory as _


class IRecaptchaedContent(Interface):
    """Just some content type with a captcha"""

    # -*- schema definition goes here -*-
    Text = schema.Text(
        title=_(u"Text"),
        required=True,
        description=_(u"Field description"),
    )
#
