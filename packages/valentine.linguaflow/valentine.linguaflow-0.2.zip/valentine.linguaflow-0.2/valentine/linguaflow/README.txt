valentine.linguaflow
====================

Translation invalidation / validation
------------------------------------

We prepare languages, we will have english as default and swedish and
polish as available languages for translation.

  >>> from Products.CMFCore.utils import getToolByName
  >>> lt = getToolByName(portal, 'portal_languages')
  >>> lt.manage_setLanguageSettings('en', ('en','sv','pl'))

Now we create some content and translations.
 
  >>> portal = self.portal
  >>> folder = portal.folder
  >>> did = folder.invokeFactory('Document', id='doc1', title="Doc one", text='Some doc one text')
  >>> did = folder.invokeFactory('Document', id='doc2', title="Doc two", text='Some doc two text')
  >>> doc1 = folder.doc1
  >>> doc2 = folder.doc2
  
  >>> doc1.addTranslation('sv')
  >>> doc1_sv = doc1.getTranslation('sv')
  >>> doc1.addTranslation('pl')
  >>> doc1_pl = doc1.getTranslation('pl')

  >>> doc1_sv.setTitle('Dok ett')
  >>> doc1_sv.setText('Lite dok ett text')

valentine.linguaflow provides a new workflow which installs as a second default workflow so all
content types that use the default one will automaticall have it.

  >>> wf = getToolByName(portal, 'portal_workflow')
  >>> linguaflow = wf.linguaflow
 
Let check status on our fresh content.

  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1)
  >>> hist[0]['review_state']
  'valid'

  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1_sv)
  >>> hist[0]['review_state']
  'valid'

Translation invalidation
~~~~~~~~~~~~~~~~~~~~~~~~

Now if we edit the canonical we can invalidate all translations.

  >>> doc1.processForm(values={'text':'Changed text of doc one'})
  >>> wf.doActionFor(doc1_sv, 'invalidate', comment='Fields changed: text')
  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1_sv)
  >>> hist[1]['review_state']
  'invalid'

  >>> hist[1]['comments']
  'Fields changed: text'

Translation validation
~~~~~~~~~~~~~~~~~~~~~~

  >>> doc1_sv.processForm(values={'text':'Translation updated'})
  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1_sv)
  >>> hist[-1]['review_state']
  'invalid'

The translation is still invalid even if we have edited and that is because a
validation has to be manually invoked when editing is done through plone since
we don't know if our changes are small corrections or retranslation of changes
in canonical.

  >>> wf.doActionFor(doc1_sv, 'validate')
  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1_sv)
  >>> hist[-1]['review_state']
  'valid'

  >>> wf.getInfoFor(doc1_sv, 'review_state', None, linguaflow.getId())
  'valid'

  
Synchronization
---------------

With LinguaPlone translations are independent objects and language independent 
fields are maintained by LinguaPlone but if you want to synchronize other 
properties like workflow_state, criteria in a SmartFolder/Topic/Collection (all
those names for same thing), zmi properites, default page or layout then 
the synchronization in valentine.linguaflow will help you.

Workflow synchronization
~~~~~~~~~~~~~~~~~~~~~~~~

If we return to our documents created above we can se that they have default 
state in their default workflow.

  >>> wf.getInfoFor(doc1, 'review_state')
  'visible'
  >>> wf.getInfoFor(doc1_sv, 'review_state')
  'visible'
  >>> wf.getInfoFor(doc1_pl, 'review_state')
  'visible'

Now we change the state of the canonical and we'll see that the translations didn't follow:

  >>> wf.doActionFor(doc1, 'publish', comment='Original text published')
  >>> wf.getInfoFor(doc1, 'review_state')
  'published'
  >>> wf.getInfoFor(doc1_sv, 'review_state')
  'visible'
  >>> wf.getInfoFor(doc1_pl, 'review_state')
  'visible'

  >>> doc1.reindexObject()
  >>> doc1_sv.reindexObject()
  >>> doc1_pl.reindexObject()

But now a manager can go to manage_translation_form and synchronize the workflow state.

  >>> from Products.PloneTestCase.setup import portal_owner, default_password
  >>> from Products.Five.testbrowser import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> self.portal.error_log._ignored_exceptions = ()
  >>> browser.open(self.portal.absolute_url())
  >>> browser.getControl(name='__ac_name').value = portal_owner
  >>> browser.getControl(name='__ac_password').value = default_password
  >>> browser.getControl(name='submit').click()
  >>> browser.open(doc1_sv.absolute_url() + '/edit') 
  >>> browser.contents
  '...">Public Draft</span>...'

  >>> browser.open(doc1_sv.absolute_url() + '/manage_translations_form') 
  >>> label = 'Svenska (sv): %s' % doc1_sv.Title()
  >>> browser.getControl(label).selected = True
  >>> browser.getControl('Expiration date').selected = True
  >>> browser.getControl('Effective date').selected = True
  >>> browser.getControl(name='linguaflow_syncworkflow:method').click()

  >>> wf.getInfoFor(doc1, 'review_state')
  'published'
  >>> [p['name'] for p in doc1.permissionsOfRole('Anonymous') 
  ...    if p['selected'] ]
  ['Access contents information', 'View']
  >>> wf.getInfoFor(doc1_sv, 'review_state')
  'published'
  >>> [p['name'] for p in doc1_sv.permissionsOfRole('Anonymous') 
  ...    if p['selected'] ]
  ['Access contents information', 'View']
  >>> wf.getInfoFor(doc1_pl, 'review_state')
  'visible'

In your code you can sync with event

  >>> from valentine.linguaflow.events import SyncWorkflowEvent
  >>> from zope.event import notify
  >>> notify(SyncWorkflowEvent(doc1, doc1_pl, comment='event sync'))
  >>> wf.getInfoFor(doc1_pl, 'review_state')
  'published'


Sync local roles to translations

  >>> doc1.get_local_roles()
  (('test_user_1_', ('Owner',)),)  
  >>> doc1.manage_setLocalRoles('tester', ('Manager',))
  >>> doc1.get_local_roles()
  (('test_user_1_', ('Owner',)), ('tester', ('Manager',)))
  >>> doc1_sv.manage_setLocalRoles('tester2', ('Manager',))
  >>> doc1_sv.get_local_roles()
  (('test_user_1_', ('Owner',)), ('tester2', ('Manager',)))

  >>> browser.open(doc1_sv.absolute_url() + '/manage_translations_form') 
  >>> label = 'Svenska (sv): %s' % doc1_sv.Title()
  >>> browser.getControl(label).selected = True
  >>> label = 'Polski (pl): %s' % doc1_pl.Title()
  >>> browser.getControl(label).selected = True
  >>> browser.getControl('Local roles').selected = True
  >>> browser.getControl(name='linguaflow_syncworkflow:method').click()

  >>> doc1_sv.get_local_roles()
  (('test_user_1_', ('Owner',)), ('tester', ('Manager',)))
  >>> doc1_pl.get_local_roles()
  (('test_user_1_', ('Owner',)), ('tester', ('Manager',)))

