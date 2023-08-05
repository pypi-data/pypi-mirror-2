from DateTime import DateTime

from zope.component import getMultiAdapter
from zope.app.form.browser import ASCIIWidget
from zope.app.form.interfaces import ConversionError
from zope.app.form.browser.textwidgets import renderElement
from zope.i18n import MessageFactory

from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

from quintagroup.captcha.core.utils import decrypt, parseKey, encrypt1, getWord

_ = MessageFactory('quintagroup.formlib.captcha')


class CaptchaWidget(ASCIIWidget):
    def __call__(self):
        context = self.context.context

        kwargs = {'type': self.type,
                  'name': self.name,
                  'id': self.name,
                  'cssClass': self.cssClass,
                  'style': self.style,
                  'size': self.displayWidth,
                  'extra': self.extra}

        portal_url = getToolByName(context, 'portal_url')()
        key = context.getCaptcha()

        if self._prefix:
            prefix = '%s.' % self._prefix
        else:
            prefix = ''

        return u"""<input type="hidden" value="%s" name="%shashkey" />
                   %s
                   <img src="%s/getCaptchaImage/%s" alt="Enter the word"/>""" % (key,
                                                                                 prefix,
                                                                                 renderElement(self.tag, **kwargs),
                                                                                 portal_url,
                                                                                 key)
         
    def _toFieldValue(self, input):
        # Verify the user input against the captcha
        context = self.context.context
        request = context.REQUEST
        
        # get captcha type (static or dynamic)
        captcha_type = context.getCaptchaType()
        
        # validate captcha input
        if input and captcha_type in ['static', 'dynamic']:
            # make up form prefix
            if self._prefix:
                prefix = '%s.' % self._prefix
            else:
                prefix = ''
            
            hashkey = request.get('%shashkey' % prefix, '')
            decrypted_key = decrypt(context.captcha_key, hashkey)
            parsed_key = parseKey(decrypted_key)
            
            index = parsed_key['key']
            date = parsed_key['date']
            
            if captcha_type == 'static':
                img = getattr(context, '%s.jpg' % index)
                solution = img.title
                enc = encrypt1(input)
            else:
                enc = input
                solution = getWord(int(index))
            
            captcha_tool = getToolByName(context, 'portal_captchas')
            if (enc != solution) or (captcha_tool.has_key(decrypted_key)) or (DateTime().timeTime() - float(date) > 3600):
                raise ConversionError(_(u'Please re-enter validation code.'))
            else:
                captcha_tool.addExpiredKey(decrypted_key)
        
        return super(CaptchaWidget, self)._toFieldValue(input)
