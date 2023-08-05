Introduction - valentine.linguaflow
===================================

With this product your multilingual site will have the information to know 
 
 * what translations are invalidate
 * what has changed
 * when was the change made

If you use XLIFFMarshal to export/import your translations it will also 
automatically use this product to validate/re-invalidate a translation.

How does it work
________________

"Suppose to work" - not there yet, automatic invalidation is disabled as default

valentine.linguaflow uses the capabilities of using multiple workflows for each
content type. It ads a second workflow which has two transitions and states, 
invalidate/validate and invalid/valid. Every time a canonical content is changed
subscribers will check if and language dependent fields have changed. If so
it will invoke invalidate transition on each translation. In the comment of the
transition it will save a diff of what has changed.

Dependencies
____________

Plone 2.5.x or Plone 3.x
LinguaPlone

Credits
-------

Funding and deployment:
  EEA_ - European Enviroment Agency (Antonio De Marinis)


Design and Development:
  `Valentine Web Systems`_ (Sasha Vincic)

.. _EEA: http://www.eea.europa.eu/
.. _Valentine Web Systems: http://valentinewebsystems.com/
