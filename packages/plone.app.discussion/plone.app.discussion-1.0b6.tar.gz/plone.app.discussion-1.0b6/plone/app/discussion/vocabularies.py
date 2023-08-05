from zope import interface
import zope.schema.interfaces
import zope.schema.vocabulary

from plone.app.discussion.interfaces import _ 

HAS_CAPTCHA = False
try:
    import plone.formwidget.captcha
    HAS_CAPTCHA = True
except ImportError:
    pass

HAS_RECAPTCHA = False
try:
    import plone.formwidget.recaptcha
    HAS_RECAPTCHA = True
except ImportError:
    pass

HAS_AKISMET = False
try:
    import collective.akismet
    HAS_AKISMET = True
except ImportError:
    pass


def captcha_vocabulary(context):
    """Vocabulary with all available captcha implementations.
    """
    terms = []
    terms.append(
        zope.schema.vocabulary.SimpleTerm(
            value='disabled',
            token='disabled',
            title=_(u'Disabled')))

    if HAS_CAPTCHA:
        terms.append(
            zope.schema.vocabulary.SimpleTerm(
                value='captcha',
                token='captcha',
                title='Captcha'))
    if HAS_RECAPTCHA:
        terms.append(
            zope.schema.vocabulary.SimpleTerm(
                value='recaptcha',
                token='recaptcha',
                title='ReCaptcha'))
    if HAS_AKISMET:
        terms.append(
            zope.schema.vocabulary.SimpleTerm(
                value='akismet',
                token='akismet',
                title='Akismet'))    
    
    return zope.schema.vocabulary.SimpleVocabulary(terms)

interface.alsoProvides(captcha_vocabulary,
                       zope.schema.interfaces.IVocabularyFactory)