from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget

from AccessControl import ClassSecurityInfo

class CaptchaWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "recaptchawidget",
        })

    security = ClassSecurityInfo()


registerWidget(CaptchaWidget,
               title='Captcha',
               description='Renders a captcha from collective.recaptcha',
               used_for=('Products.Archetypes.Field.CaptchaField',)
               )

