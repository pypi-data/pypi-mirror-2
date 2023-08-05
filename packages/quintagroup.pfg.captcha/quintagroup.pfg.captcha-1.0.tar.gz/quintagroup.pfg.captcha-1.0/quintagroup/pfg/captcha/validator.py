from Products.CMFCore.utils import getToolByName
from Products.validation import validation, interfaces

from Products.CMFPlone.utils import safe_hasattr

class CaptchaValidator:

    __implements__ = (interfaces.ivalidator,)

    name = 'CaptchaValidator'

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):

        form  = kwargs.get('instance')
        portal = getToolByName(form, 'portal_url').getPortalObject()
        result = portal.captcha_validator()
        if result.status == 'failure':
            return ("%(problem)s" % {'problem' : result.errors['key'][0]})
        else:
            return 1

validation.register(CaptchaValidator('isCaptchaCorrect'))
