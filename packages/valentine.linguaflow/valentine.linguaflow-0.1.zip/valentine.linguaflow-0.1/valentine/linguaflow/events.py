from zope.interface import Attribute, implements
from zope.component import getMultiAdapter
from zope.app.event.interfaces import IObjectEvent

from Products.CMFCore.utils import getToolByName

class ITranslationObjectUpdate(IObjectEvent):
    """ A canonical lingaua plone object has changed or a translation has
        been updated. . """

    object = Attribute("The canonical object.")
    translation = Attribute("The translation target object.")
    action = Attribute("The workflow action to perform.")
    comment = Attribute("The workflow comment, should contain which fields have changed.")

class TranslationObjectUpdate(object):
    """Sent after an canonical or translation object has been edited.
       When a canonical is edited the action is 'invalidate' and if
       a translation is edited the action is 'validate'. Both actions
       are performed on the translation."""
    implements(ITranslationObjectUpdate)

    def __init__(self, context, translation, action, comment):
        self.object = context
        self.translation = translation
        self.action = action
        self.comment = comment

def notifyCanonicalUpdate(obj, event):
    # catch all ITranslatable modified
    if event.comment:
        wt = getToolByName(obj, 'portal_workflow')
        if 'linguaflow' in wt.getChainFor(obj):
            wt.doActionFor(event.translation, event.action, comment=event.comment )


class ISyncWorkflowEvent(IObjectEvent):
    """ Make sure translation workflow status is the same as canonicals. """

    object = Attribute("The canonical object.")
    translation = Attribute("The translation target object.")
    comment = Attribute("The workflow comment, should contain which fields have changed.")


class SyncWorkflowEvent(object):
    """ """

    implements(ISyncWorkflowEvent)

    def __init__(self, context, translation, comment):
        self.object = context
        self.translation = translation
        self.comment = comment

def syncronizeTranlationWorkflow(obj, event):
    view = getMultiAdapter((obj, obj.REQUEST), name=u"linguaflow_syncworkflow")
    view.languages = [event.translation.Language()]
    view.sync(syncWorkflowState=True, comment=event.comment)
        
    
