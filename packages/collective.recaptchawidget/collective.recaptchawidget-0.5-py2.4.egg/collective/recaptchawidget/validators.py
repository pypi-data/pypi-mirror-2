from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite

from Products.validation.interfaces.IValidator import IValidator

VALID_CAPTCHA = 'very_valid'

class CaptchaValidator(object):
    __implements__ = IValidator

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title
        self.description = description

    def __call__(self, value, *args, **kwargs):
        site = getSite()
        if site.REQUEST.get('captcha_is_valid') == VALID_CAPTCHA:
            return 1
        captcha = getMultiAdapter(
            (site, site.REQUEST), name='captcha')
        if captcha.verify():
            site.REQUEST['captcha_is_valid'] = VALID_CAPTCHA
            return 1
        else:
            return 'Captcha value is not correct.'

