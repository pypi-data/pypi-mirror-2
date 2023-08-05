from zope.event import notify

from md5 import md5

from collective.monkey.monkey import Patcher
from valentine.linguaflow.events import TranslationObjectUpdate


linguaPatcher = Patcher('LinguaPlone')

#LinguaPlone patches
from Products.LinguaPlone.I18NBaseObject import *

def processForm(self, data=1, metadata=0, REQUEST=None, values=None):
    """ Find out what language dependent fields have changed. """
    outdated = self.isOutdated()

    request = REQUEST or self.REQUEST
    if values:
        form = values
    else:
        form = request.form
    fieldset = form.get('fieldset', None)
    schema = self.Schema()
    schemata = self.Schemata()
    fields = []

    if fieldset is not None:
        fields = schemata[fieldset].fields()
    else:
        if data: fields += schema.filterFields(isMetadata=0)

    form_keys = form.keys()
    oldValues = {}
    for field in fields:
        if not field.languageIndependent and field.getName() in form_keys:
            # we have a translatable field in the form
            # save a hash for old value
            accessor = field.getAccessor(self)
            oldValues[field.getName()] = md5(str(accessor())).hexdigest()
            
    # START LinguaPlone.I18NBaseObject.processForm method
    is_new_object = self.checkCreationFlag()
    BaseObject.processForm(self, data, metadata, REQUEST, values)

    #
    # Translation invalidation moved to the end
    #
    
    if self._at_rename_after_creation and is_new_object:
        new_id = self._renameAfterCreation()
    else:
        new_id = self.getId()

    if shasattr(self, '_lp_default_page'):
        delattr(self, '_lp_default_page')
        if not self.isCanonical():
            language = self.getLanguage()
            canonical = self.getCanonical()
            canonical_parent = aq_parent(aq_inner(canonical))
            parent = aq_parent(aq_inner(self))
            if parent == canonical_parent and not parent.hasTranslation(language):
                parent.addTranslation(language)
                translation_parent = parent.getTranslation(language)
                values = {'title': self.Title()}
                translation_parent.processForm(values=values)
                translation_parent.setDescription(self.Description())
                parent = translation_parent
            if shasattr(parent, 'setDefaultPage'):
                parent.setDefaultPage(new_id)

            
    if shasattr(self, '_lp_outdated'):
        delattr(self, '_lp_outdated')
    # END - LinguaPlone.I18NBaseObject.processForm method

    changedFields = []
    for fName, md5Hex in oldValues.items():
        if md5Hex != md5(str(schema.getField(fName).getAccessor(self)())).hexdigest():
            # translatable field changed
            changedFields.append(fName)

    if config.AUTO_NOTIFY_CANONICAL_UPDATE:
        comment = 'Fields changed: %s' % ','.join(changedFields)
        if self.isCanonical() and changedFields:
            self.invalidateTranslations(comment)
            # mark canonical with the changes but no state change
            cUpdate = TranslationObjectUpdate(self, self,'nochange',
                                              comment=comment)
            notify(cUpdate)


def invalidateTranslations(self, comment=''):
    """Marks the translation as outdated."""
    translations = self.getNonCanonicalTranslations()
    for lang in translations.keys():
        translation = translations[lang][0]
        translation.notifyCanonicalUpdate()
        if comment:
            cUpdate = TranslationObjectUpdate(self, translation,'invalidate',
                                              comment=comment)
            notify(cUpdate)
    self.invalidateTranslationCache()


linguaPatcher.wrap_method(I18NBaseObject, 'invalidateTranslations', invalidateTranslations)
linguaPatcher.wrap_method(I18NBaseObject, 'processForm', processForm)

