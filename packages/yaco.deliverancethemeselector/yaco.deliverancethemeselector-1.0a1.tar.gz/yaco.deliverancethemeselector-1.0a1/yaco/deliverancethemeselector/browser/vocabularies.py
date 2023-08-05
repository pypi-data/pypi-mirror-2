from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from yaco.deliverancethemeselector.interfaces \
    import IDeliveranceThemeSelectorSettings



class AvailableThemesVocabulary(object):
    """Vocabulary factory for available sectors
    """
    implements(IVocabularyFactory)

    def __call__(self, context):

        registry = getUtility(IRegistry)
        DTSSettings = registry.forInterface(IDeliveranceThemeSelectorSettings)
        items = DTSSettings.availableThemes or []
        items = [i.split(':') for i in items if len(i.split(':')) > 0]
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items if i[0]]
        return SimpleVocabulary(items)

AvailableThemesVocabularyFactory = AvailableThemesVocabulary()

